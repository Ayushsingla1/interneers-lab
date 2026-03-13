from abc import ABC, abstractmethod
from typing import List

from ...entities.product import Product, ProductCategory, ProductCategoryUpdateRequest


class CategoryServicePorts(ABC):
    @abstractmethod
    def get_all(self, page: int, limit: int) -> List[ProductCategory]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> ProductCategory:
        pass

    @abstractmethod
    def add(self, item: ProductCategory) -> ProductCategory:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self, id: str, item: ProductCategoryUpdateRequest):
        pass

    @abstractmethod
    def get_all_products(self, id: str) -> List[Product]:
        pass

    @abstractmethod
    def get_product(self, id: str, product_id: str) -> Product:
        pass
