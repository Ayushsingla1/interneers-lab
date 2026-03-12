class ProductRepositoryError(Exception):
    pass


class ProductNotFoundError(ProductRepositoryError):
    pass
