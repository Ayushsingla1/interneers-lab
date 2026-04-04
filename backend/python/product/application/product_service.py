import json
from base64 import b64decode, urlsafe_b64encode
from datetime import datetime

from product.application.dto.products.inbound.request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from product.application.dto.products.inbound.response import (
    ProductResponse,
    ProductsResponse,
)
from product.application.dto.products.outbound.request import (
    ProductCreationData,
    ProductUpdateData,
)
from product.application.dto.products.outbound.response import ProductsRepoResponse
from product.application.mappers.product_mapper import (
    map_product_to_response,
    map_products_to_responses,
)
from product.application.ports.incoming import product_service_port
from product.application.ports.outgoing.category_repo_port import (
    CategoryRepositoryPorts,
)
from product.application.ports.outgoing.product_repo_port import ProductRepositoryPorts
from .ports.outgoing.cursor_ports import CursorPaginationPorts
from product.domain.custom_exceptions import InvalidIdError
from product.domain.entities.product import Product


class ProductService(product_service_port.ProductServicePorts):
    def __init__(
        self,
        product_repository: ProductRepositoryPorts,
        category_repository: CategoryRepositoryPorts,
        cursor_repository: CursorPaginationPorts,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.cursor_repository = cursor_repository

    def get_all(
        self,
        limit: int,
        cursor: str | None,
        category: str | None,
        created_after: datetime | None,
    ) -> ProductsRepoResponse:

        id = None
        date = None
        if cursor is not None:
            decoded_cursor = self.cursor_repository.decode(cursor)
            id = decoded_cursor.id
            date = decoded_cursor.created_at

        if category is not None:
            category = self.category_repository.get_by_name(category)

        repo_response = self.product_repository.get_all(
            id=id,
            limit=limit,
            category=category,
            date=date,
            created_after=created_after,
        )
        products = repo_response.products

        next_cursor = None

        if repo_response.has_more:
            last_id = repo_response.products[-1].id
            last_created_at = repo_response.products[-1].created_at
            next_cursor = self.cursor_repository.encode(
                id=last_id, created_at=last_created_at
            )

        return ProductsResponse(
            products=map_products_to_responses(products),
            next_cursor=next_cursor,
            has_more=repo_response.has_more,
        )

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
