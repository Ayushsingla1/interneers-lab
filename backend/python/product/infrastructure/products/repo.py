from datetime import UTC, datetime
from typing import List

from mongoengine import DoesNotExist, NotUniqueError, OperationError, ConnectionFailure

from product.application.dto.products.outbound.request import ProductCreationData, ProductUpdateData
from product.domain.custom_exceptions import (
    ProductNotFoundError,
    ProductRepositoryError,
    ProductNotUniqueError
)
from product.domain.entities.product import Product
from product.application.ports.outgoing import product_repo_port
from ..validations import _validate_object_id

from ..models import ProductDocument
from .mapping import _to_document_product, _to_entity_product

class ProductRepository(product_repo_port.ProductRepositoryPorts):
    def get_by_id(self, id: str) -> Product:
        oid = _validate_object_id(id, "ProductId")
        try:
            document = ProductDocument.objects.get(id=oid)
            return _to_entity_product(document)
        except ConnectionFailure as e:
            raise ProductRepositoryError("Unable to connect to database server") from e
        except DoesNotExist:
            raise ProductNotFoundError(f"No product found with Id {id}")
        except OperationError as e:
            raise ProductRepositoryError("Database operation failed while fetching the product") from e
        except Exception as e:
            raise ProductRepositoryError("Unexpected error while fetching the product") from e

    def get_all(self, start: int, end: int, category: str | None, date : datetime | None) -> List[Product]:
        filters = {}
        if category is not None:
            filters["category"] = _validate_object_id(category, "CategoryId")
        if date is not None:
            filters["created_at__gt"] = date
        try:
            documents = list(ProductDocument.objects(**filters)[start:end])
            products = []
            for doc in documents:
                products.append(_to_entity_product(doc))
            return products
        except ConnectionFailure as e:
            raise ProductRepositoryError("Unable to connect to database server") from e
        except OperationError as e:
            raise ProductRepositoryError("Database operation failed while fetching the products") from e
        except Exception as e:
            raise ProductRepositoryError("Unexpected error while fetching the product") from e


    def add(self, item: ProductCreationData) -> Product:
        try:
            document = _to_document_product(item)
            document.save()
            return _to_entity_product(document)
        except ConnectionFailure as e:
            raise ProductRepositoryError("Unable to connect to database server") from e
        except NotUniqueError as e:
            raise ProductNotUniqueError("Product should be unique") from e
        except OperationError as e:
            raise ProductRepositoryError("Database operation failed while saving the products") from e
        except Exception as e:
            raise ProductRepositoryError("Unexpected error while saving the product") from e

    def delete(self, id: str):
        oid = _validate_object_id(id, "ProductId")
        try:
            deleted = ProductDocument.objects(id=oid).delete()
            if deleted == 0:
                raise ProductNotFoundError(f"No product with id: {id}")
        except ConnectionFailure as e:
            raise ProductRepositoryError("Unable to connect to database server") from e
        except ProductNotFoundError:
            raise
        except OperationError as e:
            raise ProductRepositoryError("Database operation failed while deleting the products") from e
        except Exception as e:
            raise ProductRepositoryError("Unexpected error while deleting the product") from e

    def update(self, id : str, item: ProductUpdateData):
        oid = _validate_object_id(id, "ProductId")
        try:
            update_items = {f"set__{k}": v for k, v in item.fields_to_change().items()}
            update_items["set__updated_at"] = datetime.now(tz=UTC)
            updated = ProductDocument.objects(id=oid).update_one(
                **update_items
            )
            if updated == 0:
                raise ProductNotFoundError(f"No product with id: {id}")
        except ConnectionFailure as e:
            raise ProductRepositoryError("Unable to connect to database server") from e
        except ProductNotFoundError:
            raise 
        except NotUniqueError as e:
            raise ProductNotUniqueError("Product should be unique") from e
        except OperationError as e:
            raise ProductRepositoryError("Database operation failed while updating the products") from e
        except Exception as e:
            raise ProductRepositoryError("Unexpected error while updating the product") from e
