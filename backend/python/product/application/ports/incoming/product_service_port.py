from abc import ABC, abstractmethod
from datetime import datetime

from product.application.dto.products.inbound.request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from product.application.dto.products.inbound.response import ProductResponse
from product.application.dto.products.outbound.response import ProductsRepoResponse


class ProductServicePorts(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> ProductResponse:
        pass

    @abstractmethod
    def get_all(
        self,
        cursor: str | None,
        limit: int,
        category: str | None,
        created_after: datetime | None,
    ) -> ProductsRepoResponse:
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
