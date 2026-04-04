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
from product.application.ports.outgoing import category_repo_port, product_repo_port
from product.application.mappers.category_mapper import (
    map_category_to_response,
    map_categories_to_responses,
)
from product.application.mappers.product_mapper import (
    map_product_to_response,
    map_products_to_responses,
)


class CategoryService(category_service_port.CategoryServicePorts):
    def __init__(
        self,
        category_repository: category_repo_port.CategoryRepositoryPorts,
        product_repository: product_repo_port.ProductRepositoryPorts,
    ):
        self.category_repository = category_repository
        self.product_repository = product_repository

    def get_all(self, page: int, limit: int) -> List[CategoryResponse]:
        start = (page - 1) * limit
        end = start + limit
        categories = self.category_repository.get_all(start, end)
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
        date = None
        if cursor is not None:
            decoded_token = json.loads(b64decode(cursor).decode("utf-8"))
            if decoded_token is not None and decoded_token["id"] is not None:
                product_id = decoded_token["id"]
                date = datetime.fromisoformat(decoded_token["date"])
            else:
                raise InvalidToken("Token sent is invalid")

        repo_response = self.product_repository.get_all(
            product_id, limit, id, date, None
        )

        next_cursor = None
        if repo_response.has_more:
            json_cursor = json.dumps(
                {
                    "id": repo_response.products[-1].id,
                    "date": repo_response.products[-1].created_at.isoformat(),
                }
            )
            next_cursor = urlsafe_b64encode(json_cursor.encode("utf-8")).decode("utf-8")
        return ProductsResponse(
            map_products_to_responses(repo_response.products),
            next_cursor,
            repo_response.has_more,
        )

    def get_product(self, id: str, product_id: str) -> ProductResponse:
        product_data = self.category_repository.get_product(id, product_id)
        return map_product_to_response(product_data)
