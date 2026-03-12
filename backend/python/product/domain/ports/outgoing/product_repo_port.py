from abc import ABC, abstractmethod
from typing import List

from ...entities.product import Product, ProductUpdateRequest


class ProductRepositoryPorts(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Product:
        pass

    @abstractmethod
    def get_all(self, start: int, end: int) -> List[Product]:
        pass

    @abstractmethod
    def add(self, item: Product) -> Product:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self, id: str, item: ProductUpdateRequest):
        pass
