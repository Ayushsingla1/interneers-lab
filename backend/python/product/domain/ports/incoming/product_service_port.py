from abc import ABC, abstractmethod
from typing import List

from product.shared.dto.products.request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from product.shared.dto.products.response import ProductResponse


class ProductServicePorts(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> ProductResponse:
        pass

    @abstractmethod
    def get_all(self, page: int, limit: int, category: str) -> List[ProductResponse]:
        pass

    @abstractmethod
    def add(self, item: CreateProductRequest) -> ProductResponse:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self, id: str, item: UpdateProductRequest):
        pass
