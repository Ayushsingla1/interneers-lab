from typing import List
from mongoengine import DoesNotExist, ConnectionFailure, NotUniqueError, OperationError
from mongoengine.base.fields import ObjectId

from product.application.dto.category.outbound.request import CategoryCreationData, CategoryUpdateData
from product.domain.custom_exceptions import (
    CategoryNotFoundError,
    CategoryNotUniqueError,
    CategoryRepositoryError,
)
from product.domain.entities.product import Product
from product.domain.entities.category import Category
from product.application.ports.outgoing import category_repo_port

from .mapping import _to_document_category, _to_entity_category
from ..products.mapping import _to_entity_product
from ..models import CategoryDocument, ProductDocument
from ..validations import _validate_object_id


class CategoryRepository(category_repo_port.CategoryRepositoryPorts):
    def get_all(self, start: int, end: int) -> List[Category]:
        try:
            documents = list(CategoryDocument.objects[start:end])
            products = []
            for doc in documents:
                products.append(_to_entity_category(doc))
            return products
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except OperationError as e:
            raise CategoryRepositoryError("Database operation failed while fetching the category") from e
        except Exception as e:
            raise CategoryRepositoryError("Unexpected Error while fetching the category") from e

    def get_by_id(self, id: str) -> Category:
        oid = _validate_object_id(id, "CategoryId")
        try:
            document = CategoryDocument.objects.get(id=oid)
            return _to_entity_category(document)
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except DoesNotExist:
            raise CategoryNotFoundError(f"No category found with Id {id}")
        except OperationError as e:
            raise CategoryRepositoryError("Database operation failed while fetching the category") from e
        except Exception as e:
            raise CategoryRepositoryError("Unable to fetch Category") from e

    def add(self, item: CategoryCreationData) -> Category:
        try:
            document = _to_document_category(item)
            document.save()
            return _to_entity_category(document)
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except NotUniqueError as e:
            raise CategoryNotUniqueError("Category should be unique") from e
        except OperationError as e:
            raise CategoryRepositoryError("Database operation failed while creating the category") from e
        except Exception as e:
            raise CategoryRepositoryError("Unable to save category") from e

    def delete(self, id: str):
        oid = _validate_object_id(id, "CategoryId")
        try:
            deleted = CategoryDocument.objects(id=oid).delete()
            if deleted == 0:
                raise CategoryNotFoundError(f"No category with id: {id}")
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except OperationError as e:
            raise CategoryRepositoryError("Database operation failed while deleting the category") from e
        except CategoryNotFoundError:
            raise
        except Exception as e:
            raise CategoryRepositoryError("Unable to delete category") from e

    def update(self, id, item: CategoryUpdateData):
        oid = _validate_object_id(id, "CategoryId")
        try:
            update_items = {f"set__{k}": v for k, v in item.fields_to_change().items()}
            updated = CategoryDocument.objects(id=oid).update_one(
                **update_items
            )
            if updated == 0:
                raise CategoryNotFoundError(f"No category with id: {id}")
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except NotUniqueError as e:
            raise CategoryNotUniqueError("Category should be unique") from e
        except CategoryNotFoundError:
            raise
        except OperationError as e:
            raise CategoryRepositoryError("Database operation failed while updating the category") from e
        except Exception as e:
            raise CategoryRepositoryError("Unable to update category") from e

    def get_all_products(self, id: str) -> List[Product]:
        oid = _validate_object_id(id, "CategoryId")
        try:
            docs = list(ProductDocument.objects(category=oid))
            products = []
            for doc in docs:
                products.append(_to_entity_product(doc))
            return products
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except OperationError as e:
            raise CategoryRepositoryError("Database operation failed while fetching the category products") from e
        except Exception as e:
            raise CategoryRepositoryError("Database error") from e

    def get_product(self, id: str, product_id: str) -> Product:
        coid = _validate_object_id(id, "CategoryId")
        poid = _validate_object_id(product_id, "ProductId")
        try:
            docs = ProductDocument.objects(
                id=poid, category=coid
            ).select_related().get()
            return _to_entity_product(docs)
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except DoesNotExist:
            raise CategoryNotFoundError("Unable to find category with such id") from e
        except OperationError as e:
            raise CategoryRepositoryError("Database operation failed while updating the category") from e
        except Exception as e:
            raise CategoryRepositoryError("Database error") from e

    def get_by_name(self, name: str) -> str:
        try:
            docs = CategoryDocument.objects.get(title = name)
            return docs.id
        except ConnectionFailure as e:
            raise CategoryRepositoryError("Unable to connect to db") from e
        except DoesNotExist:
            raise CategoryNotFoundError("No category with such name") from e
        except Exception as e:
            raise CategoryRepositoryError("Database error") from e
            
