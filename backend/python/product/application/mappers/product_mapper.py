from typing import List
from product.domain.entities.product import Product
from product.shared.dto.products.response import ProductResponse


def map_product_to_response(product: Product) -> ProductResponse:
    """Map Product entity to ProductResponse DTO"""
    return ProductResponse(
        id=str(product.id) if product.id else "",
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=(
            int(product.quantity)
            if isinstance(product.quantity, str)
            else product.quantity
        ),
        category=product.category,
    )


def map_products_to_responses(products: List[Product]) -> List[ProductResponse]:
    """Map list of Product entities to list of ProductResponse DTOs"""
    return [map_product_to_response(product) for product in products]
