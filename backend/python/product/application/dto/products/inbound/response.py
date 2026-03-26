from dataclasses import dataclass


@dataclass
class ProductResponse:
    id: str
    name: str
    description: str
    price: float
    quantity: int
    category: str
