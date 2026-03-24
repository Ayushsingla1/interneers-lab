from typing import List
from product.domain.entities.category import Category
from product.shared.dto.category.response import CategoryResponse


def map_category_to_response(category: Category) -> CategoryResponse:
    """Map Category entity to CategoryResponse DTO"""
    return CategoryResponse(
        id=str(category.id) if category.id else "",
        title=category.title,
        description=category.description,
    )


def map_categories_to_responses(categories: List[Category]) -> List[CategoryResponse]:
    """Map list of Category entities to list of CategoryResponse DTOs"""
    return [map_category_to_response(category) for category in categories]
