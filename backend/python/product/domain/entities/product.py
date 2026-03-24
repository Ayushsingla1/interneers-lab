from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    name: str
    description: str
    quantity: int
    price: float
    category: str
    brand: str
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.price <= 0:
            raise ValueError("Product price should be greater than 0")
        if self.quantity <= 0:
            raise ValueError("Product quantity should be greater than 0")
