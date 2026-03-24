from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateProductRequest:
    name: str
    description: str
    quantity: str
    price: float
    category: str
    brand: str

    def __post_init__(self):

        if not self.price or self.price <= 0:
            raise ValueError("Price should always be greater than 0")

        if not self.quantity or self.quantity <= 0:
            raise ValueError("quantity should always be greater than 0")

        if not self.brand or self.brand.strip() is None:
            raise ValueError("Brand name cannot be empty")

        if not self.name or self.name.strip() is None:
            raise ValueError("name cannot be empty")

        if not self.description or self.description.strip() is None:
            raise ValueError("description cannot be empty")

        if not self.category or self.category.strip() is None:
            raise ValueError("category cannot be empty")


@dataclass
class UpdateProductRequest:

    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None

    def __post_init__(self):

        if self.price is not None and self.price <= 0:
            raise ValueError("Price should always be greater than 0")

        if self.quantity is not None and self.quantity <= 0:
            raise ValueError("quantity should always be greater than 0")

        if self.brand is not None and self.brand.strip() is None:
            raise ValueError("Brand name cannot be empty")

        if self.name is not None and self.name.strip() is None:
            raise ValueError("name cannot be empty")

        if self.description is not None and self.description.strip() is None:
            raise ValueError("description cannot be empty")

        if self.category is not None and self.category.strip() is None:
            raise ValueError("category cannot be empty")

    def has_changes(self) -> bool:

        for v in vars(self).values():
            if v is not None:
                return True
        return False
