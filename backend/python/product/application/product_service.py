from typing import List

from product.application.dto.products import ProductCreationData, ProductUpdateData
from product.application.mappers.product_mapper import (
    map_product_to_response,
    map_products_to_responses,
)
from product.domain.entities.product import Product
from product.domain.ports.incoming import product_service_port
from product.domain.ports.outgoing import product_repo_port
from product.shared.dto.products.request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from product.shared.dto.products.response import ProductResponse


class ProductService(product_service_port.ProductServicePorts):
    def __init__(self, product_repository: product_repo_port.ProductRepositoryPorts):
        self.product_repository = product_repository

    def get_all(self, page: int, limit: int, category: str) -> List[ProductResponse]:
        start = (page - 1) * limit
        end = start + limit
        products = self.product_repository.get_all(
            start=start, end=end, category=category
        )
        return map_products_to_responses(products)

    def get_by_id(self, id: str) -> ProductResponse:
        product: Product = self.product_repository.get_by_id(id)
        return map_product_to_response(product)

    def add(self, item: CreateProductRequest) -> ProductResponse:
        create_data = ProductCreationData(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
            brand=item.brand,
            category=item.category,
        )
        product: Product = self.product_repository.add(create_data)
        return map_product_to_response(product)

    def update(self, id: str, item: UpdateProductRequest):
        update_data = ProductUpdateData(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
            brand=item.brand,
            category=item.category,
        )
        return self.product_repository.update(id, update_data)

    def delete(self, id: str):
        return self.product_repository.delete(id)
