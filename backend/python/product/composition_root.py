from product.api.views import ProductController
from product.application.product_service import ProductService
from product.infrastructure.repo import ProductRepository

repository = ProductRepository()
service = ProductService(repository)
# controller = ProductController()

product_list = ProductController.as_view(
    {"get": "list", "post": "create"}, service=service
)

product_detail = ProductController.as_view(
    {"get": "retrieve", "delete": "destroy", "put": "put"}, service=service
)
