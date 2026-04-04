from rest_framework import serializers
from datetime import datetime


class ProductGetSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    category = serializers.CharField()


class ProductPostSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    brand = serializers.CharField()
    price = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=10)
    quantity = serializers.IntegerField(min_value=0)
    category = serializers.CharField()


class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    brand = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    price = serializers.DecimalField(
        min_value=0, decimal_places=2, max_digits=10, required=False
    )
    quantity = serializers.IntegerField(required=False, allow_null=True)
    category = serializers.CharField(required=False)


class ProductListQuerySerializer(serializers.Serializer):
    cursor = serializers.CharField(required=False)
    limit = serializers.IntegerField(
        required=False, min_value=1, max_value=100, default=10
    )
    after = serializers.DateField(required=False, input_formats=["%d-%m-%Y"])
    category = serializers.CharField(required=False)

    def validate_after(self, value):
        return datetime.combine(value, datetime.min.time())
