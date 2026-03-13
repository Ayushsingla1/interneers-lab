from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from product.application.category_service import CategoryService
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    CategoryRepositoryError,
)
from product.domain.entities.product import (
    ProductCategory,
    ProductCategoryUpdateRequest,
)
from .product_serializers import ProductGetSerializer

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
            categories = CategorySerializer(
                self.service.get_all(page=int(page), limit=int(limit)), many=True
            )
            return Response(categories.data, status=status.HTTP_200_OK)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        data = CategorySerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            valid_data: dict = data.validated_data
            category = ProductCategory(
                title=valid_data["title"],
                description=valid_data["description"],
            )

            created_category = CategorySerializer(self.service.add(category))

            return Response(status=status.HTTP_201_CREATED, data=created_category.data)
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
            category = CategorySerializer(self.service.get_by_id(id=pk))
            return Response(category.data, status=status.HTTP_200_OK)
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        data = CategoryUpdateSerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            validated_data = data.validated_data
            print(validated_data)
            updated_fields = ProductCategoryUpdateRequest(**validated_data)

            if updated_fields.has_changes():
                self.service.update(pk, updated_fields)
            else:
                raise ValidationError("No data provided to update")

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
            products_data = ProductGetSerializer(products, many=True)
            return Response(products_data.data, status=status.HTTP_200_OK)
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_product(self, request, pk, product_id):
        try:
            product = self.service.get_product(id=pk, product_id=product_id)
            product_data = ProductGetSerializer(product)
            return Response(product_data.data, status=status.HTTP_200_OK)
        except CategoryNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)