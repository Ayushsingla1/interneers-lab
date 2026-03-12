from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    brand = serializers.CharField()
    price = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=10)
    quantity = serializers.IntegerField()
    category = serializers.ListField(read_only=True)
