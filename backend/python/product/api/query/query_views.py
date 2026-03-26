

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from product.api.products.product_serializers import ProductGetSerializer
from product.application.query_service import QueryService
from product.domain.custom_exceptions import ProductRepositoryError


class QueryController(ViewSet):
    service : QueryService = None

    def list(self, request):

        try:
            description = request.query_params.get("q")
            if description is None or description.strip() == "":
                return Response(status = status.HTTP_400_BAD_REQUEST)

            products = self.service.get_related(description)
            serialized_products = ProductGetSerializer(products, many = True)
            return Response(serialized_products.data, status = status.HTTP_200_OK)

        except ProductRepositoryError as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)