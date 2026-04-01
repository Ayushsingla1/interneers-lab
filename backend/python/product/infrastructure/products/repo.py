from datetime import UTC, datetime
from typing import List
import functools
from mongoengine import DoesNotExist, NotUniqueError, OperationError, ConnectionFailure

from product.application.dto.products.outbound.request import (
    ProductCreationData,
    ProductUpdateData,
)
from product.domain.custom_exceptions import (
    InvalidIdError,
    ProductNotFoundError,
    ProductRepositoryError,
    ProductNotUniqueError,
)
from product.domain.entities.product import Product
from product.application.ports.outgoing import product_repo_port
from ..validations import _validate_object_id

from ..models import ProductDocument
from .mapping import _to_document_product, _to_entity_product


def handle_db_errors(operation: str):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ProductNotFoundError, ProductNotUniqueError, InvalidIdError):
                raise
            except ConnectionFailure as e:
                raise ProductRepositoryError(
                    "Unable to connect to database server"
                ) from e
            except DoesNotExist as e:
                raise ProductNotFoundError(f"No product found with Id") from e
            except NotUniqueError as e:
                raise ProductNotUniqueError("Product should be unique") from e
            except OperationError as e:
                raise ProductRepositoryError(
                    f"Database operation failed while {operation} the products"
                ) from e
            except Exception as e:
                raise ProductRepositoryError(
                    f"Unexpected error while {operation} the product"
                ) from e

        return wrapper

    return decorator


class ProductRepository(product_repo_port.ProductRepositoryPorts):

    @handle_db_errors("fetching")
    def get_by_id(self, id: str) -> Product:
        oid = _validate_object_id(id, "ProductId")
        document = ProductDocument.objects.get(id=oid)
        return _to_entity_product(document)

    @handle_db_errors("fetching")
    def get_all(
        self, start: int, end: int, category: str | None, date: datetime | None
    ) -> List[Product]:
        filters = {}
        if category is not None:
            filters["category"] = _validate_object_id(category, "CategoryId")
        if date is not None:
            filters["created_at__gt"] = date
        documents = list(ProductDocument.objects(**filters)[start:end])
        products = []
        for doc in documents:
            products.append(_to_entity_product(doc))
        return products

    @handle_db_errors("saving")
    def add(self, item: ProductCreationData) -> Product:
        item.category = _validate_object_id(item.category, "CategoryId")
        document = _to_document_product(item)
        document.save()
        return _to_entity_product(document)

    @handle_db_errors("deleting")
    def delete(self, id: str):
        oid = _validate_object_id(id, "ProductId")
        deleted = ProductDocument.objects(id=oid).delete()
        if deleted == 0:
            raise ProductNotFoundError(f"No product with id: {id}")

    @handle_db_errors("updating")
    def update(self, id: str, item: ProductUpdateData):
        oid = _validate_object_id(id, "ProductId")
        update_items = {f"set__{k}": v for k, v in item.fields_to_change().items()}
        update_items["set__updated_at"] = datetime.now(tz=UTC)
        updated = ProductDocument.objects(id=oid).update_one(**update_items)
        if updated == 0:
            raise ProductNotFoundError(f"No product with id: {id}")
