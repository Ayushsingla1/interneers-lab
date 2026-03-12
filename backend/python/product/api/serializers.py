from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    brand = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    price = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=10)
    quantity = serializers.IntegerField()
    category = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )


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
    category = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
