from typing import List
from base64 import b64decode, urlsafe_b64encode
from datetime import datetime
import json
from product.application.dto.category.inbound.request import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from product.application.dto.category.inbound.response import CategoryResponse
from product.application.dto.products.inbound.response import (
    ProductResponse,
    ProductsResponse,
)
from product.application.dto.category.outbound.request import (
    CategoryCreationData,
    CategoryUpdateData,
)
from product.application.ports.incoming import category_service_port
from product.application.ports.outgoing.category_repo_port import (
    CategoryRepositoryPorts,
)
from product.application.ports.outgoing.product_repo_port import ProductRepositoryPorts
from product.application.mappers.category_mapper import (
    map_category_to_response,
    map_categories_to_responses,
)
from product.application.mappers.product_mapper import (
    map_product_to_response,
    map_products_to_responses,
)
from .ports.outgoing.cursor_ports import CursorPaginationPorts


class CategoryService(category_service_port.CategoryServicePorts):
    def __init__(
        self,
        category_repository: CategoryRepositoryPorts,
        product_repository: ProductRepositoryPorts,
        cursor_repository: CursorPaginationPorts,
    ):
        self.category_repository = category_repository
        self.product_repository = product_repository
        self.cursor_repository = cursor_repository

    def get_all(self) -> List[CategoryResponse]:
        categories = self.category_repository.get_all()
        return map_categories_to_responses(categories)

    def get_by_id(self, id: str) -> CategoryResponse:
        category = self.category_repository.get_by_id(id)
        return map_category_to_response(category)

    def add(self, item: CreateCategoryRequest) -> CategoryResponse:
        category_data = CategoryCreationData(
            title=item.title, description=item.description
        )
        category = self.category_repository.add(category_data)
        return map_category_to_response(category)

    def update(self, id: str, item: UpdateCategoryRequest):

        category = CategoryUpdateData(title=item.title, description=item.description)

        return self.category_repository.update(id, category)

    def delete(self, id: str):
        return self.category_repository.delete(id)

    def get_all_products(self, id: str, cursor: str, limit: str) -> ProductsResponse:

        product_id = None
        created_at = None
        if cursor is not None:
            decoded_cursor = self.cursor_repository.decode(cursor)
            product_id = decoded_cursor.id
            created_at = decoded_cursor.created_at

        repo_response = self.product_repository.get_all(
            product_id, limit, id, created_at, None
        )

        next_cursor = None
        if repo_response.has_more:
            last_id = repo_response.products[-1].id
            last_created_at = repo_response.products[-1].created_at
            next_cursor = self.cursor_repository.encode(
                id=last_id, created_at=last_created_at
            )

        return ProductsResponse(
            products=map_products_to_responses(repo_response.products),
            next_cursor=next_cursor,
            has_more=repo_response.has_more,
        )

    def get_product(self, id: str, product_id: str) -> ProductResponse:
        product_data = self.category_repository.get_product(id, product_id)
        return map_product_to_response(product_data)
