from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Product:
    name: str
    description: str
    quantity: int
    price: float
    brand: Optional[str] = None
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.price <= 0:
            raise ValueError("Product price should be greater than 0")
        if self.quantity <= 0:
            raise ValueError("Product quantity should be greater than 0")


@dataclass
class ProductUpdateRequest:
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[List[str]] = None

    def has_changes(self) -> bool:
        for val in vars(self).values():
            if val is not None:
                return True
        return False

    def fields_to_change(self):
        return {k: v for k, v in vars(self).items() if v is not None}
