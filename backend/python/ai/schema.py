from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    """Information regarding toys"""

    name: str = Field(description="Name of the toy", min_length=3)
    description: str = Field(description="Information about the toy", min_length=10)
    brand: str = Field(description="Brand of the toy", min_length=3)
    price: float = Field(description="Price of the toy", gt=0)
    quantity: int = Field(description="Quantity of toy in stock", gt=0)


class ProductOutputSchema(BaseModel):
    products: list[ProductSchema] = Field(description="Contains the toys", min_length=1)
