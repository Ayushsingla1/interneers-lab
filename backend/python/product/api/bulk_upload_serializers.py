from rest_framework import serializers


class BulkProductUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file")
        return value


class BulkUploadResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    created = serializers.IntegerField()
    errors = serializers.IntegerField()
    products = serializers.ListField(child=serializers.DictField(), required=False)
    error_details = serializers.ListField(child=serializers.DictField(), required=False)
