from django.urls import path

from .product_repository import ProductRepository
from .product_service import ProductServices
from .views import ProductController

repository = ProductRepository()
service = ProductServices(repository=repository)

product_list = ProductController.as_view(
    {"get": "list", "post": "create"}, service=service
)

product_detail = ProductController.as_view(
    {"get": "retrieve", "delete": "destroy", "put": "put"}, service=service
)

urlpatterns = [
    path("products/", product_list, name="product-list"),
    path("products/<str:pk>/", product_detail, name="product-detail"),
]
