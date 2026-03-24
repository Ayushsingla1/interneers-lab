from product.api.products.product_views import ProductController
from product.api.category.category_views import CategoryController
from product.api.products.bulk_upload_views import BulkProductUploadController
from product.application.product_service import ProductService
from product.application.category_service import CategoryService
from product.infrastructure.products.repo import ProductRepository
from product.infrastructure.category.repo import CategoryRepository

product_repository = ProductRepository()
product_service = ProductService(product_repository)

category_repository = CategoryRepository()
category_service = CategoryService(category_repository)

product_list = ProductController.as_view(
    {"get": "list", "post": "create"}, service=product_service
)

product_detail = ProductController.as_view(
    {"get": "retrieve", "delete": "destroy", "put": "put"}, service=product_service
)

category_list = CategoryController.as_view(
    {"get": "list", "post": "create"}, service=category_service
)

category_detail = CategoryController.as_view(
    {"get": "retrieve", "delete": "destroy", "put": "put"}, service=category_service
)

category_products = CategoryController.as_view(
    {"get": "get_products"}, service=category_service
)

category_product_detail = CategoryController.as_view(
    {"get": "get_product"}, service=category_service
)

bulk_product_upload = BulkProductUploadController.as_view(
    {"post": "create"}, service=product_service
)
