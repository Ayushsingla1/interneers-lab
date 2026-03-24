import csv
import io
from mongoengine import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from product.application.product_service import ProductService
from product.domain.custom_exceptions import ProductRepositoryError
from product.shared.dto.products.request import CreateProductRequest
from .product_serializers import ProductGetSerializer, ProductPostSerializer
from .bulk_upload_serializers import (
    BulkProductUploadSerializer,
    BulkUploadResponseSerializer,
)


class BulkProductUploadController(ViewSet):
    parser_classes = [MultiPartParser, FormParser]
    service: ProductService = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_fields(self):
        return True

    def create(self, request):
        serializer = BulkProductUploadSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            csv_file = serializer.validated_data["file"]

            file_data = csv_file.read().decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(file_data))

            created_products = []
            errors = []

            for row_num, row in enumerate(csv_reader, start=2):
                try:
                    required_fields = [
                        "name",
                        "description",
                        "price",
                        "quantity",
                        "category",
                    ]
                    missing_fields = [
                        field
                        for field in required_fields
                        if not row.get(field) or row.get(field).strip() == ""
                    ]

                    if missing_fields:
                        errors.append(
                            {
                                "row": row_num,
                                "error": f"Missing required fields: {', '.join(missing_fields)}",
                                "data": row,
                            }
                        )
                        continue

                    serialized_data = ProductPostSerializer(data = {**row})
                    serialized_data.is_valid(raise_exception=True)

                    product_request = CreateProductRequest(**serialized_data.data)
                    print(product_request)

                    created_product = self.service.add(product_request)
                    created_products.append(ProductGetSerializer(created_product).data)

                except ValidationError as e:
                    errors.append(
                        {
                            "row" : row_num,
                            "error" : f"Invalid args: {str(e)}",
                            "data" : row
                        }
                    )
                except ValueError as e:
                    errors.append(
                        {
                            "row": row_num,
                            "error": f"Invalid data format: {str(e)}",
                            "data": row,
                        }
                    )
                except ProductRepositoryError as e:
                    errors.append(
                        {
                            "row": row_num,
                            "error": f"Database error: {str(e)}",
                            "data": row,
                        }
                    )
                except Exception as e:
                    errors.append(
                        {
                            "row": row_num,
                            "error": f"Unexpected error: {str(e)}",
                            "data": row,
                        }
                    )

            response_data = {
                "message": f"Processed {len(created_products) + len(errors)} rows",
                "created": len(created_products),
                "errors": len(errors),
                "products": created_products,
            }

            if errors:
                response_data["error_details"] = errors

            response_serializer = BulkUploadResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to process CSV file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
