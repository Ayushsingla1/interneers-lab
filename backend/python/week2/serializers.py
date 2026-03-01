from rest_framework import serializers
from .models import Category, Brand, Product

class CategorySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Category
        fields = ['title']

class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name','description','price','brand','category']
    
    brand = BrandSerializer()
    category = CategorySerializer()
