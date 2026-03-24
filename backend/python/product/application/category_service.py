from typing import List

from product.shared.dto.category.request import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from product.shared.dto.category.response import CategoryResponse
from product.shared.dto.products.response import ProductResponse
from product.application.dto.category import CategoryCreationData, CategoryUpdateData
from product.domain.ports.incoming import category_service_port
from product.domain.ports.outgoing import category_repo_port
from product.application.mappers.category_mapper import (
    map_category_to_response,
    map_categories_to_responses,
)
from product.application.mappers.product_mapper import (
    map_product_to_response,
    map_products_to_responses,
)


class CategoryService(category_service_port.CategoryServicePorts):
    def __init__(self, category_repository: category_repo_port.CategoryRepositoryPorts):
        self.category_repository = category_repository

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

    def get_all_products(self, id: str) -> List[ProductResponse]:
        products = self.category_repository.get_all_products(id)
        return map_products_to_responses(products)

    def get_product(self, id: str, product_id: str) -> ProductResponse:
        product_data = self.category_repository.get_product(id, product_id)
        return map_product_to_response(product_data)
