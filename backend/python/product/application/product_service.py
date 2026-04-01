from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    ProductRepositoryError,
)
from product.application.dto.products.outbound.request import (
    ProductCreationData,
    ProductUpdateData,
)
from product.application.mappers.product_mapper import (
    map_product_to_response,
    map_products_to_responses,
)
from product.domain.entities.product import Product
from product.application.ports.incoming import product_service_port
from product.application.ports.outgoing import product_repo_port, category_repo_port
from product.application.dto.products.inbound.request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from product.application.dto.products.inbound.response import ProductResponse
from datetime import datetime
from typing import List


class ProductService(product_service_port.ProductServicePorts):
    def __init__(
        self,
        product_repository: product_repo_port.ProductRepositoryPorts,
        category_repository: category_repo_port.CategoryRepositoryPorts,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def get_all(
        self, page: int, limit: int, category: str, date: datetime | None
    ) -> List[ProductResponse]:
        start = (page - 1) * limit
        end = start + limit

        if category is not None:
            category = self.category_repository.get_by_name(category)

        products = self.product_repository.get_all(
            start=start, end=end, category=category, date=date
        )
        return map_products_to_responses(products)

    def get_by_id(self, id: str) -> ProductResponse:
        product: Product = self.product_repository.get_by_id(id)
        return map_product_to_response(product)

    def add(self, item: CreateProductRequest) -> ProductResponse:
        category_id = self.category_repository.get_by_name(item.category)
        create_data = ProductCreationData(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
            brand=item.brand,
            category=category_id,
        )
        product: Product = self.product_repository.add(create_data)
        return map_product_to_response(product)

    def update(self, id: str, item: UpdateProductRequest):

        if item.category is not None:
            category_details = self.category_repository.get_by_name(item.category)
            item.category = category_details.id

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
