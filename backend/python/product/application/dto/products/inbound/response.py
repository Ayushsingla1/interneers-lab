from dataclasses import dataclass
from typing import List


@dataclass
class ProductResponse:
    id: str
    name: str
    description: str
    price: float
    quantity: int
    category: str


@dataclass
class ProductsResponse:
    products: List[ProductResponse]
    next_cursor: str
    has_more: bool
