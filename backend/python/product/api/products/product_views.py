from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from product.application.dto.products.inbound.request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from product.application.product_service import ProductService
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    InvalidCursorError,
    ProductNotFoundError,
    ProductNotUniqueError,
    ProductRepositoryError,
)

from .product_serializers import (
    ProductGetSerializer,
    ProductListQuerySerializer,
    ProductPostSerializer,
    ProductUpdateSerializer,
)


class ProductController(ViewSet):
    service: ProductService = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        query_params = request.query_params
        serialized_query_params = ProductListQuerySerializer(data=query_params)

        try:
            serialized_query_params.is_valid(raise_exception=True)
            validated_params = serialized_query_params.validated_data
            cursor = validated_params.get("cursor")
            limit = validated_params.get("limit")
            created_after = validated_params.get("after")
            category = validated_params.get("category")

            products = self.service.get_all(
                cursor=cursor,
                limit=limit,
                created_after=created_after,
                category=category,
            )

            serializer = ProductGetSerializer(products.products, many=True)

            return Response(
                data={
                    "next_cursor": products.next_cursor,
                    "data": serializer.data,
                    "has_more": products.has_more,
                },
                status=status.HTTP_200_OK,
            )
        except (InvalidCursorError, ValidationError) as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ProductRepositoryError, Exception) as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        data = ProductPostSerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            valid_data: dict = data.validated_data
            prod = CreateProductRequest(**valid_data)
            product = self.service.add(prod)
            serializer = ProductGetSerializer(product)
            return Response(
                data={"data": serializer.data}, status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response(
                data={"error": f"unable to validate data {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (ProductNotUniqueError, CategoryNotFoundError) as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ProductRepositoryError, Exception) as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk):
        try:
            self.service.delete(id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductNotFoundError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (ProductRepositoryError, Exception) as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk):
        try:
            product = self.service.get_by_id(id=pk)
            serializer = ProductGetSerializer(product)
            return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
        except ProductNotFoundError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (ProductRepositoryError, Exception) as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        data = ProductUpdateSerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            validated_data = data.validated_data

            if not validated_data or validated_data == {}:
                raise ValidationError("No data provided to update")
            else:
                data = UpdateProductRequest(**validated_data)
                self.service.update(pk, data)
            return Response(status=status.HTTP_200_OK)
        except ValidationError:
            return Response(
                data="Data validation failed", status=status.HTTP_400_BAD_REQUEST
            )
        except ProductNotFoundError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_204_NO_CONTENT)
        except ProductNotUniqueError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ProductRepositoryError as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
