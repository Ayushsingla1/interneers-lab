from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(required = False)
    title = serializers.CharField()
    description = serializers.CharField()


class CategoryUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
