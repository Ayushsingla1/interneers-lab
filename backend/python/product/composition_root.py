from .adapters.incoming.views import ProductController
from .adapters.outgoing.repo import ProductRepository
from .services.product_service import ProductService

repository = ProductRepository()
service = ProductService(repository)
# controller = ProductController()

product_list = ProductController.as_view(
    {"get": "list", "post": "create"}, service=service
)

product_detail = ProductController.as_view(
    {"get": "retrieve", "delete": "destroy", "put": "put"}, service=service
)
