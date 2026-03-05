from typing import List

from models import Product
from product_interface import ProductInterface


class ProductServices(ProductInterface):
    def __init__(self, repository: ProductInterface):
        self.repository = repository

    def products(self) -> List[Product]:
        return self.repository.products()

    def product_by_id(self, id: str) -> Product:
        if not isinstance(id, str):
            raise ValueError("id must be a string")
        return self.repository.product_by_id(id)

    def add_product(self, **kwargs) -> Product:
        return self.repository.add_product(**kwargs)

    def delete_product(self, id: str) -> None:
        if not isinstance(id, str):
            raise ValueError("id must be a string")
        self.repository.delete_product(id)
