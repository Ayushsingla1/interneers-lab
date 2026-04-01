from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("File must be a PDF file")
        return value


class ChatSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["user", "ai"])
    text = serializers.CharField()


class ChatListSerializer(serializers.Serializer):
    chats = ChatSerializer(many=True)
