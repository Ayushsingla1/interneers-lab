from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductCreationData:
    name: str
    description: str
    price: float
    quantity: int
    brand: str
    category: str


@dataclass
class ProductUpdateData:
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    brand: Optional[str]
    category: Optional[str]

    def fields_to_change(self):
        return {k: v for k, v in vars(self).items() if v is not None}
