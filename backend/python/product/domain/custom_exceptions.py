class ProductRepositoryError(Exception):
    pass


class ProductNotFoundError(ProductRepositoryError):
    pass


class CategoryRepositoryError(Exception):
    pass


class CategoryNotFoundError(CategoryRepositoryError):
    pass
