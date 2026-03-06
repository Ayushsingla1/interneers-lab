from typing import List

from mongoengine import DoesNotExist
from mongoengine.base.fields import ObjectId

from .models import Product
from .product_interface import ProductInterface


class ProductRepositoryError(Exception):
    pass


class ProductNotFoundError(ProductRepositoryError):
    pass


class ProductRepository(ProductInterface):
    def get_all(self, **kwargs) -> List[Product]:
        try:
            return list(Product.objects[kwargs["start"] : kwargs["end"]])
        except Exception as e:
            raise ProductRepositoryError("Unable to fetch Products.") from e

    def get_by_id(self, id: str) -> Product:
        try:
            product = Product.objects.get(id=ObjectId(id))
            return product
        except DoesNotExist:
            raise ProductNotFoundError("No product with matching Id")
        except Exception as e:
            raise ProductRepositoryError("Unable to fetch Product") from e

    def add(self, **kwargs) -> Product:
        try:
            product = Product(**kwargs)
            product.save()
            return product
        except Exception as e:
            raise ProductRepositoryError("Unable to save product") from e

    def delete(self, id: str):
        try:
            deleted = Product.objects(id=ObjectId(id)).delete()
            if deleted == 0:
                raise ProductNotFoundError(f"No product with id: {id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise ProductRepositoryError("Unable to delete product") from e

    def update(self, id, **kwargs):
        try:
            updated = Product.objects(id=ObjectId(id)).update_one(**kwargs)
            if updated == 0:
                raise ProductNotFoundError(f"No product with id: {id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise ProductRepositoryError("Unable to update product") from e
