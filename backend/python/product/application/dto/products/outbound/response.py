from dataclasses import dataclass
from typing import List
from product.domain.entities.product import Product


@dataclass
class ProductsRepoResponse:
    products: List[Product]
    has_more: bool
