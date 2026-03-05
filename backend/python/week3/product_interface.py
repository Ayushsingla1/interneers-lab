from abc import ABC, abstractmethod
from typing import List

from models import Product


class ProductInterface(ABC):
    @abstractmethod
    def products(self) -> List[Product]:
        pass

    @abstractmethod
    def product_by_id(self, id: str) -> Product:
        pass

    @abstractmethod
    def add_product(self, **kwargs) -> Product:
        pass

    @abstractmethod
    def delete_product(self, id: str) -> None:
        pass
