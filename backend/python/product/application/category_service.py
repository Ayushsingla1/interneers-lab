from typing import List

from product.domain.entities.product import (
    Product,
    ProductCategory,
    ProductCategoryUpdateRequest,
)
from product.domain.ports.incoming import category_service_port
from product.domain.ports.outgoing import category_repo_port


class CategoryService(category_service_port.CategoryServicePorts):
    def __init__(self, category_repository: category_repo_port.CategoryRepositoryPorts):
        self.category_repository = category_repository

    def get_all(self, page: int, limit: int) -> List[ProductCategory]:
        start = (page - 1) * limit
        end = start + limit
        return self.category_repository.get_all(start, end)

    def get_by_id(self, id: str) -> ProductCategory:
        return self.category_repository.get_by_id(id)

    def add(self, item: ProductCategory) -> ProductCategory:
        return self.category_repository.add(item)

    def update(self, id: str, item: ProductCategoryUpdateRequest):
        return self.category_repository.update(id, item)

    def delete(self, id: str):
        return self.category_repository.delete(id)

    def get_all_products(self, id: str) -> List[Product]:
        return self.category_repository.get_all_products(id)

    def get_product(self, id: str, product_id: str) -> Product:
        return self.category_repository.get_product(id, product_id)
