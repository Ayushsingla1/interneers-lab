from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from product.shared.dto.category.request import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from product.application.category_service import CategoryService
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    CategoryRepositoryError,
)
from .category_serializers import CategorySerializer, CategoryUpdateSerializer


def isParsable(val) -> int | None:

    if isinstance(val, int):
        return val

    try:
        val = int(val)
        return val
    except Exception:
        return None


class CategoryController(ViewSet):
    service: CategoryService = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        query_params = request.query_params
        page = query_params.get("page") or 1
        limit = query_params.get("limit") or 10

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
            categories = self.service.get_all(page=int(page), limit=int(limit))
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        data = CategorySerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            validated_data: dict = data.validated_data

            category = CreateCategoryRequest(**validated_data)

            created_category = self.service.add(category)
            serializer = CategorySerializer(created_category)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        except ValidationError as e:
            return Response(
                data="unable to validate data", status=status.HTTP_400_BAD_REQUEST
            )
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        try:
            self.service.delete(id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        try:
            category = self.service.get_by_id(id=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        data = CategoryUpdateSerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            validated_data = data.validated_data
            data = UpdateCategoryRequest(**validated_data)
            if not validated_data or validated_data == {}:
                raise ValidationError("No data provided to update")
            else:
                self.service.update(pk, data)
            return Response(status=status.HTTP_200_OK)
        except ValidationError:
            return Response(
                data="Data validation failed", status=status.HTTP_400_BAD_REQUEST
            )
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_products(self, request, pk):
        try:
            products = self.service.get_all_products(id=pk)
            from product.api.products.product_serializers import ProductGetSerializer

            serializer = ProductGetSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_product(self, request, pk, product_id):
        try:
            product = self.service.get_product(id=pk, product_id=product_id)
            from product.api.products.product_serializers import ProductGetSerializer

            serializer = ProductGetSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
