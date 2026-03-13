from django.urls import path

from product.composition_root import (
    product_detail, 
    product_list,
    category_list,
    category_detail,
    category_products,
    category_product_detail
)

urlpatterns = [
    path("products/", product_list, name="product-list"),
    path("products/<str:pk>/", product_detail, name="product-detail"),
    path("categories/", category_list, name="category-list"),
    path("categories/<str:pk>/", category_detail, name="category-detail"),
    path("categories/<str:pk>/products/", category_products, name="category-products"),
    path("categories/<str:pk>/products/<str:product_id>/", category_product_detail, name="category-product-detail"),
]
