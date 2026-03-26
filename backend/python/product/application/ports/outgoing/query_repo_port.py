from abc import ABC, abstractmethod
from typing import List
from product.domain.entities.product import Product

class QueryRepositoryPorts(ABC):

    @abstractmethod
    def get_related(self, description: str) -> List[str]:
        pass

    @abstractmethod
    def add(self, products: List[Product]):
        pass