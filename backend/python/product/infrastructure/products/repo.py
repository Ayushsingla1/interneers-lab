from datetime import UTC, datetime
from typing import List

from mongoengine import DoesNotExist
from mongoengine.base.fields import ObjectId

from product.application.dto.products import ProductCreationData, ProductUpdateData
from product.domain.custom_exceptions import (
    ProductNotFoundError,
    ProductRepositoryError,
)
from product.domain.entities.product import Product
from product.domain.ports.outgoing import product_repo_port

from ..models import ProductDocument
from .mapping import _to_document_product, _to_entity_product


class ProductRepository(product_repo_port.ProductRepositoryPorts):

    def get_by_id(self, id: str) -> Product:
        try:
            document = ProductDocument.objects.get(id=ObjectId(id))
            print(document)
            return _to_entity_product(document)
        except DoesNotExist:
            raise ProductNotFoundError("No product with matching Id")
        except Exception as e:
            raise ProductRepositoryError("Unable to fetch Product") from e

    def get_all(self, start: int, end: int, category: str = None) -> List[Product]:
        try:
            filters = {}
            if category is not None:
                cat_obj = CategoryDocument.objects(title=category)[0]
                if cat_obj:
                    filters["category"] = cat_obj.id
                else:
                    return []

            documents = list(ProductDocument.objects(**filters)[start:end])
            products = []
            for doc in documents:
                products.append(_to_entity_product(doc))
            return products
        except Exception as e:
            raise ProductRepositoryError("Unable to fetch Products.") from e

    def add(self, item: ProductCreationData) -> Product:
        try:
            document = _to_document_product(item)
            document.save()
            return _to_entity_product(document)
        except Exception as e:
            raise ProductRepositoryError("Unable to save product") from e

    def delete(self, id: str):
        try:
            deleted = ProductDocument.objects(id=ObjectId(id)).delete()
            if deleted == 0:
                raise ProductNotFoundError(f"No product with id: {id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise ProductRepositoryError("Unable to delete product") from e

    def update(self, id, item: ProductUpdateData):
        try:
            update_items = {f"set__{k}": v for k, v in item.fields_to_change().items()}
            update_items["set__updated_at"] = datetime.now(tz=UTC)
            print("hi", update_items)
            updated = ProductDocument.objects(id=ObjectId(id)).update_one(
                **update_items
            )
            print(updated)
            if updated == 0:
                raise ProductNotFoundError(f"No product with id: {id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise ProductRepositoryError("Unable to update product") from e
