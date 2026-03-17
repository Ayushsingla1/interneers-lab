from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from product.application.product_service import ProductService
from product.domain.custom_exceptions import (
    ProductNotFoundError,
    ProductRepositoryError,
)
from product.shared.dto.products.request import (
    CreateProductRequest,
    UpdateProductRequest,
)

from .product_serializers import (
    ProductGetSerializer,
    ProductPostSerializer,
    ProductUpdateSerializer,
)


def isParsable(val) -> int | None:

    if isinstance(val, int):
        return val

    try:
        val = int(val)
        return val
    except Exception:
        return None


class ProductController(ViewSet):
    service: ProductService = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        query_params = request.query_params
        page = query_params.get("page") or 1
        limit = query_params.get("limit") or 10
        category = query_params.get("category")

        if isParsable(page) is None or int(page) == 0:
            return Response(
                "Page should be integer and greater than 0",
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif isParsable(limit) is None or int(limit) == 0:
            return Response(
                "Limit should be integer and greater than 0",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            products = self.service.get_all(
                page=int(page), limit=int(limit), category=category
            )
            serializer = ProductGetSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        data = ProductPostSerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            valid_data: dict = data.validated_data
            prod = CreateProductRequest(**valid_data)
            product = self.service.add(prod)
            serializer = ProductGetSerializer(product)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

        except ValidationError as e:
            return Response(
                data="unable to validate data", status=status.HTTP_400_BAD_REQUEST
            )
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        try:
            self.service.delete(id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        try:
            product = self.service.get_by_id(id=pk)
            serializer = ProductGetSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
