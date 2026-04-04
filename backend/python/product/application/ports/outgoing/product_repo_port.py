from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from torch._inductor.ir import NoneAsConstantBuffer

from product.application.dto.products.outbound.request import (
    ProductCreationData,
    ProductUpdateData,
)
from product.application.dto.products.outbound.response import ProductsRepoResponse
from product.domain.entities.product import Product


class ProductRepositoryPorts(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Product:
        pass

    @abstractmethod
    def get_all(
        self,
        id: str | None,
        limit: int,
        category: str | None,
        date: datetime | None,
        created_after: datetime | None,
    ) -> ProductsRepoResponse:
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
