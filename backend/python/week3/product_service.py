from typing import List

from .models import Product
from .product_interface import ProductInterface


class ProductServices(ProductInterface):
    def __init__(self, repository: ProductInterface):
        self.repository = repository

    def get_all(self, **kwargs) -> List[Product]:
        start = (kwargs["page"] - 1) * kwargs["limit"]
        end = start + kwargs["limit"]
        return self.repository.get_all(start=start, end=end)

    def get_by_id(self, id: str) -> Product:
        if not isinstance(id, str):
            raise ValueError("id must be a string")
        return self.repository.get_by_id(id)

    def add(self, **kwargs) -> Product:
        return self.repository.add(**kwargs)

    def delete(self, id: str):
        if not isinstance(id, str):
            raise ValueError("id must be a string")
        self.repository.delete(id)

    def update(self, id: str, **kwargs):
        update_fields = {f"set__{k}": v for k, v in kwargs.items()}
        return self.repository.update(id, **update_fields)
