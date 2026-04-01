class ProductRepositoryError(Exception):
    pass


class ProductNotFoundError(ProductRepositoryError):
    pass


class CategoryRepositoryError(Exception):
    pass


class CategoryNotFoundError(CategoryRepositoryError):
    pass


class ProductNotUniqueError(ProductRepositoryError):
    pass


class InvalidIdError(ProductRepositoryError, CategoryRepositoryError):
    pass


class CategoryNotUniqueError(CategoryRepositoryError):
    pass
