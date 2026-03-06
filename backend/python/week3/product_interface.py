from abc import ABC, abstractmethod
from typing import List

from .models import Product


class ProductInterface(ABC):
    @abstractmethod
    def get_all(self, **kwargs) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Product:
        pass

    @abstractmethod
    def add(self, **kwargs) -> Product:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def update(self, id, **kwargs) -> None:
        pass
