from typing import List
from mongoengine import DoesNotExist, ConnectionFailure, NotUniqueError, OperationError

from product.application.dto.category.outbound.request import (
    CategoryCreationData,
    CategoryUpdateData,
)
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    CategoryNotUniqueError,
    CategoryRepositoryError,
    InvalidIdError,
)
from product.domain.entities.product import Product
from product.domain.entities.category import Category
from product.application.ports.outgoing import category_repo_port

from .mapping import _to_document_category, _to_entity_category
from ..products.mapping import _to_entity_product
from ..models import CategoryDocument, ProductDocument
from ..validations import _validate_object_id
import functools


def handle_db_errors(operation: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (CategoryNotFoundError, CategoryNotUniqueError, InvalidIdError):
                raise
            except ConnectionFailure as e:
                raise CategoryRepositoryError(
                    "Unable to connect to database server"
                ) from e
            except DoesNotExist as e:
                raise CategoryNotFoundError(f"No category found with Id") from e
            except NotUniqueError as e:
                raise CategoryNotUniqueError("Category should be unique") from e
            except OperationError as e:
                raise CategoryRepositoryError(
                    f"Database operation failed while {operation} the category"
                ) from e
            except Exception as e:
                raise CategoryRepositoryError(
                    f"Unexpected Error while {operation} the category"
                ) from e

        return wrapper

    return decorator


class CategoryRepository(category_repo_port.CategoryRepositoryPorts):

    @handle_db_errors("fetching")
    def get_all(self, start: int, end: int) -> List[Category]:
        documents = list(CategoryDocument.objects[start:end])
        products = []
        for doc in documents:
            products.append(_to_entity_category(doc))
        return products

    @handle_db_errors("fetching")
    def get_by_id(self, id: str) -> Category:
        oid = _validate_object_id(id, "CategoryId")
        document = CategoryDocument.objects.get(id=oid)
        return _to_entity_category(document)

    @handle_db_errors("creating")
    def add(self, item: CategoryCreationData) -> Category:
        document = _to_document_category(item)
        document.save()
        return _to_entity_category(document)

    @handle_db_errors("deleting")
    def delete(self, id: str):
        oid = _validate_object_id(id, "CategoryId")
        deleted = CategoryDocument.objects(id=oid).delete()
        if deleted == 0:
            raise CategoryNotFoundError(f"No category with id: {id}")

    @handle_db_errors("updating")
    def update(self, id, item: CategoryUpdateData):
        oid = _validate_object_id(id, "CategoryId")
        update_items = {f"set__{k}": v for k, v in item.fields_to_change().items()}
        updated = CategoryDocument.objects(id=oid).update_one(**update_items)
        if updated == 0:
            raise CategoryNotFoundError(f"No category with id: {id}")

    @handle_db_errors("fetching")
    def get_product(self, id: str, product_id: str) -> Product:
        coid = _validate_object_id(id, "CategoryId")
        poid = _validate_object_id(product_id, "ProductId")
        docs = ProductDocument.objects(id=poid, category=coid).select_related().get()
        return _to_entity_product(docs)

    @handle_db_errors("fetching")
    def get_by_name(self, name: str) -> str:
        docs = CategoryDocument.objects.get(title=name)
        return str(docs.id)
