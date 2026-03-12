from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from product.domain.entities.product import Product
from product.services.product_service import ProductService

from ..custom_exceptions import ProductNotFoundError, ProductRepositoryError
from ..serializers import ProductSerializer


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
            products = ProductSerializer(
                self.service.get_all(page=int(page), limit=int(limit)), many=True
            )
            return Response(products.data, status=status.HTTP_200_OK)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        print("hi")
        data = ProductSerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            valid_data: dict = data.validated_data

            print(valid_data["name"])

            prod = Product(
                name=valid_data["name"],
                description=valid_data["description"],
                price=valid_data["price"],
                quantity=valid_data["quantity"],
                brand=valid_data["brand"],
            )

            print(prod)

            product = ProductSerializer(self.service.add(prod))
            return Response(status=status.HTTP_201_CREATED, data=product.data)
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
            product = ProductSerializer(self.service.get_by_id(id=pk))
            return Response(product.data, status=status.HTTP_200_OK)
        except ProductNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        data = ProductSerializer(data=request.data, partial=True)
        try:
            data.is_valid(raise_exception=True)
            validated_data = data.validated_data
            print(validated_data)
            if validated_data == {}:
                raise ValidationError("No fields provided to updated")
            self.service.update(id=pk, **validated_data)
            return Response(status=status.HTTP_200_OK)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
