from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from product.application.dto.products.outbound.request import (
    ProductCreationData,
    ProductUpdateData,
)
from product.domain.entities.product import Product


class ProductRepositoryPorts(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Product:
        pass

    @abstractmethod
    def get_all(
        self, start: int, end: int, category: str | None, date: datetime | None
    ) -> List[Product]:
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
