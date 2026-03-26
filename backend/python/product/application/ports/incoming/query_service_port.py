from abc import ABC, abstractmethod
from typing import List
from product.application.dto.products.inbound.response import ProductResponse

class QueryServicePorts(ABC):

    @abstractmethod
    def get_related(self, description : str) -> List[ProductResponse]:
        pass
