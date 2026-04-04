from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from product.application.product_service import ProductService
from datetime import datetime
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    InvalidToken,
    ProductNotFoundError,
    ProductNotUniqueError,
    ProductRepositoryError,
)
from product.application.dto.products.inbound.request import (
    CreateProductRequest,
    UpdateProductRequest,
)

from .product_serializers import (
    ProductGetSerializer,
    ProductPostSerializer,
    ProductUpdateSerializer,
)


def isParsable(val) -> bool:
    if isinstance(val, int):
        return val
    try:
        val = int(val)
        return True
    except Exception:
        return False


def is_valid_date(val) -> bool:
    try:
        datetime.strptime(val, "%d-%m-%Y")
        return True
    except:
        return False


class ProductController(ViewSet):
    service: ProductService = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        query_params = request.query_params
        category = query_params.get("category")
        cursor = query_params.get("cursor")
        limit = query_params.get("limit") or 10
        created_after = query_params.get("after")

        if not isParsable(limit) or int(limit) == 0:
            return Response(
                data="Limit should be integer and greater than 0",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if created_after is not None and not is_valid_date(created_after):
            return Response(
                data="Provide date in dd-mm-yyyy format",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            created_after = (
                datetime.strptime(created_after, "%d-%m-%Y")
                if created_after is not None
                else None
            )
            products = self.service.get_all(
                cursor=cursor,
                limit=int(limit),
                category=category,
                created_after=created_after,
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
        except InvalidToken as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        except ProductRepositoryError as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        except ProductNotUniqueError as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        except CategoryNotFoundError as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        try:
            self.service.delete(id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductNotFoundError as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
        except ProductRepositoryError as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        try:
            product = self.service.get_by_id(id=pk)
            serializer = ProductGetSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductNotFoundError as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
        except ProductRepositoryError as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response(data=str(e), status=status.HTTP_204_NO_CONTENT)
        except ProductNotUniqueError as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        except ProductRepositoryError as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
