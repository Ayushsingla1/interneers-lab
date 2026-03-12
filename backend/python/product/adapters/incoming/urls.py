from django.urls import path

from product.composition_root import product_detail, product_list

urlpatterns = [
    path("products/", product_list, name="product-list"),
    path("products/<str:pk>/", product_detail, name="product-detail"),
]
