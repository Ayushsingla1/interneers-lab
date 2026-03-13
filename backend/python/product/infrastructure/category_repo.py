from datetime import UTC, datetime
from typing import List

from mongoengine import DoesNotExist
from mongoengine.base.fields import ObjectId

import product
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    CategoryRepositoryError,
    ProductNotFoundError,
    ProductRepositoryError,
)
from product.domain.entities.product import (
    Product,
    ProductCategory,
    ProductCategoryUpdateRequest,
)
from product.domain.ports.outgoing import category_repo_port

from .category_mapping import _to_document_category, _to_entity_category
from .product_mapping import _to_entity_product
from .models import CategoryDoument, ProductDocument


class CategoryRepository(category_repo_port.CategoryRepositoryPorts):
    def get_all(self, start: int, end: int) -> List[ProductCategory]:
        try:
            documents = list(CategoryDoument.objects[start:end])
            products = []
            for doc in documents:
                products.append(_to_entity_category(doc))
            return products
        except Exception as e:
            raise CategoryRepositoryError("Unable to fetch Categories.") from e

    def get_by_id(self, id: str) -> ProductCategory:
        try:
            document = CategoryDoument.objects.get(id=ObjectId(id))
            return _to_entity_category(document)
        except DoesNotExist:
            raise CategoryNotFoundError("No category with matching Id")
        except Exception as e:
            raise CategoryRepositoryError("Unable to fetch Category") from e

    def add(self, item: ProductCategory) -> ProductCategory:
        try:
            document = _to_document_category(item)
            document.save()
            return _to_entity_category(document)
        except Exception as e:
            raise CategoryRepositoryError("Unable to save category") from e

    def delete(self, id: str):
        try:
            deleted = CategoryDoument.objects(id=ObjectId(id)).delete()
            if deleted == 0:
                raise CategoryNotFoundError(f"No category with id: {id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise CategoryRepositoryError("Unable to delete category") from e

    def update(self, id, item: ProductCategoryUpdateRequest):
        try:
            update_items = {f"set__{k}": v for k, v in item.fields_to_change().items()}
            updated = CategoryDoument.objects(id=ObjectId(id)).update_one(
                **update_items
            )
            if updated == 0:
                raise CategoryNotFoundError(f"No category with id: {id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise CategoryRepositoryError("Unable to update category") from e

    def get_all_products(self, id: str) -> List[Product]:
        try:
            docs = list(ProductDocument.objects(category = ObjectId(id)).select_related())
            products = []
            for doc in docs:
                products.append(_to_entity_product(doc))
            return products
        except DoesNotExist:
            raise CategoryNotFoundError("Unable to find category with such id")
        except Exception as e:
            raise CategoryRepositoryError("Database error") from e

    def get_product(self, id: str, product_id: str) -> Product:
        try:
            docs = ProductDocument.objects(id = ObjectId(product_id), category = ObjectId(id)).select_related()
            return _to_entity_product(docs[0])
        except DoesNotExist:
            raise CategoryNotFoundError("Unable to find category with such id")
        except Exception as e:
            raise CategoryRepositoryError("Database error") from e
