from abc import ABC, abstractmethod
from typing import List
from product.application.dto.category import CategoryCreationData, CategoryUpdateData

from ...entities.product import Product
from ...entities.category import Category


class CategoryRepositoryPorts(ABC):
    @abstractmethod
    def get_all(self, page: int, limit: int) -> List[Category]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Category:
        pass

    @abstractmethod
    def add(self, item: CategoryCreationData) -> Category:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self, id: str, item: CategoryUpdateData):
        pass

    @abstractmethod
    def get_all_products(self, id: str) -> List[Product]:
        pass

    @abstractmethod
    def get_product(self, id: str, product_id: str) -> Product:
        pass
