from abc import ABC, abstractmethod
from typing import List

from product.application.dto.products import ProductCreationData, ProductUpdateData

from ...entities.product import Product


class ProductRepositoryPorts(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Product:
        pass

    @abstractmethod
    def get_all(self, page: int, limit: int, category: str = None) -> List[Product]:
        pass

    @abstractmethod
    def add(self, item: ProductCreationData) -> Product:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self, id: str, item: ProductUpdateData):
        pass
