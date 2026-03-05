from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .product_interface import ProductInterface
from .product_repository import (
    ProductNotFoundError,
    ProductRepositoryError,
)
from .serializers import ProductSerializer


class ProductController(ViewSet):
    service: ProductInterface

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        try:
            products = ProductSerializer(self.service.products(), many=True)
            return Response(products.data, status=status.HTTP_201_CREATED)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk: str):
        try:
            product = ProductSerializer(self.service.product_by_id(id=pk))
            return Response(product.data, status=status.HTTP_200_OK)
        except ProductNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        print(request.data)
        try:
            product = ProductSerializer(self.service.add_product(**request.data))
            return Response(status=status.HTTP_200_OK, data=product.data)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        try:
            self.service.delete_product(id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ProductRepositoryError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ProductsController(APIView):
#     def __init__(self, service: ProductInterface):
#         self.service = service

#     def get(self, request, id):

#         if not id:

#         else:


#     def post(self, request):
