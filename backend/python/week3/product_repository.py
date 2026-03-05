from mongoengine import DoesNotExist
from mongoengine.base.fields import ObjectId

from .models import Product
from .product_interface import ProductInterface


class ProductRepositoryError(Exception):
    pass


class ProductNotFoundError(ProductRepositoryError):
    pass


class ProductRepository(ProductInterface):
    def products(self):
        try:
            return list(Product.objects)
        except Exception as e:
            raise ProductRepositoryError("Unable to fetch Products.") from e

    def product_by_id(self, id: str) -> Product:
        try:
            product = Product.objects.get(id=ObjectId(id))
            return product
        except DoesNotExist:
            raise ProductNotFoundError("No product with matching Id")
        except Exception as e:
            raise ProductRepositoryError("Unable to fetch Product") from e

    def add_product(self, **kwargs) -> Product:
        try:
            product = Product(**kwargs)
            product.save()
            return product
        except Exception as e:
            raise ProductRepositoryError("Unable to save product") from e

    def delete_product(self, id: str):
        try:
            deleted = Product.objects(id=ObjectId(id)).delete()
            print(deleted)
            if deleted == 0:
                raise ProductNotFoundError(f"No product with id: {id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise ProductRepositoryError("Unable to delete product") from e
