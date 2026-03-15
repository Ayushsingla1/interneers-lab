from abc import ABC, abstractmethod
from typing import List

from product.shared.dto.category.request import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from product.shared.dto.category.response import CategoryResponse
from product.shared.dto.products.response import ProductResponse


class CategoryServicePorts(ABC):
    @abstractmethod
    def get_all(self, page: int, limit: int) -> List[CategoryResponse]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> CategoryResponse:
        pass

    @abstractmethod
    def add(self, item: CreateCategoryRequest) -> CategoryResponse:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self, id: str, item: UpdateCategoryRequest):
        pass

    @abstractmethod
    def get_all_products(self, id: str) -> List[ProductResponse]:
        pass

    @abstractmethod
    def get_product(self, id: str, product_id: str) -> ProductResponse:
        pass
