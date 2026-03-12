from typing import List

from product.domain.entities.product import Product, ProductUpdateRequest
from product.domain.ports.incoming import product_service_port
from product.domain.ports.outgoing import product_repo_port


class ProductService(product_service_port.ProductServicePorts):
    def __init__(self, product_repository: product_repo_port.ProductRepositoryPorts):
        self.product_repository = product_repository

    def get_all(self, page: int, limit: int) -> List[Product]:
        start = (page - 1) * limit
        end = start + limit
        return self.product_repository.get_all(start, end)

    def get_by_id(self, id: str) -> Product:
        return self.product_repository.get_by_id(id)

    def add(self, item: Product) -> Product:
        return self.product_repository.add(item)

    def update(self, id: str, item: ProductUpdateRequest):
        return self.product_repository.update(id, item)

    def delete(self, id: str):
        return self.product_repository.delete(id)
