from rest_framework import viewsets
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        if(request.user and request.user.is_staff):
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED, data = b'Only Admin can add products')
    
    def update(self, request, *args, **kwargs):
        if(request.user and request.user.is_staff):
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED, data = b'Only Admin can update products')


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer