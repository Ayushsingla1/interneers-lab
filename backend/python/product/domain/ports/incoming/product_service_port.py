from abc import ABC, abstractmethod
from typing import List

from ...entities.product import Product, ProductUpdateRequest


class ProductServicePorts(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Product:
        pass

    @abstractmethod
    def get_all(self, page: int, limit: int, category: str = None) -> List[Product]:
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
