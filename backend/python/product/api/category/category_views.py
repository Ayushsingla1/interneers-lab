from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from product.api.products.product_serializers import ProductGetSerializer
from product.application.dto.category.inbound.request import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from product.application.category_service import CategoryService
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    CategoryNotUniqueError,
    CategoryRepositoryError,
)
from .category_serializers import (
    CategorySerializer,
    CategoryUpdateSerializer,
    CategoryGetProductsQuerySerializer,
)


class CategoryController(ViewSet):
    service: CategoryService = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        try:
            categories = self.service.get_all()
            serializer = CategorySerializer(categories, many=True)
            return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
        except CategoryRepositoryError as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
                data=f"unable to validate data {str(e)}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CategoryNotUniqueError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CategoryRepositoryError as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk):
        try:
            self.service.delete(id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CategoryNotFoundError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk):
        try:
            category = self.service.get_by_id(id=pk)
            serializer = CategorySerializer(category)
            return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
        except CategoryNotFoundError as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
        except CategoryNotFoundError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except CategoryNotUniqueError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_products(self, request, pk):
        query_params = request.query_params
        serialized_data = CategoryGetProductsQuerySerializer(data=query_params)
        try:
            serialized_data.is_valid(raise_exception=True)
            validated_params = serialized_data.validated_data
            cursor = validated_params.get("cursor")
            limit = validated_params.get("limit")
            products = self.service.get_all_products(id=pk, cursor=cursor, limit=limit)
            serializer = ProductGetSerializer(products.products, many=True)
            return Response(
                {
                    "data": serializer.data,
                    "has_more": products.has_more,
                    "next_cursor": products.next_cursor,
                },
                status=status.HTTP_200_OK,
            )
        except CategoryNotFoundError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (ValidationError, CategoryRepositoryError) as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_product(self, request, pk, product_id):
        try:
            product = self.service.get_product(id=pk, product_id=product_id)
            serializer = ProductGetSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CategoryNotFoundError as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
        except CategoryRepositoryError as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
