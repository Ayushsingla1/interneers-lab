from product.domain.custom_exceptions import ProductRepositoryError
from product.application.ports.outgoing.product_repo_port import ProductRepositoryPorts
from product.application.ports.incoming.query_service_port import QueryServicePorts
from product.application.ports.outgoing.query_repo_port import QueryRepositoryPorts
from product.application.dto.products.inbound.response import ProductResponse
from product.application.mappers.product_mapper import map_products_to_responses
from typing import List


class QueryService(QueryServicePorts):

    def __init__(
        self,
        query_repository: QueryRepositoryPorts,
        product_repository: ProductRepositoryPorts,
    ):
        self.query_repository = query_repository
        self.product_repository = product_repository
        self.add()

    def get_related(self, description: str) -> List[ProductResponse]:

        response = self.query_repository.get_related(description)
        products = []
        for id in response:
            products.append(self.product_repository.get_by_id(id))
        return map_products_to_responses(products)

    def add(self):
        products = self.product_repository.get_all(0, 100, None, None)
        self.query_repository.add(products)
