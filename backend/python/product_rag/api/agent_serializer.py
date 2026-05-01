from rest_framework import serializers


class AgentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("File must be a PDF file")
        return value


class AgentChatSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["user", "ai"])
    text = serializers.CharField()


class AgentQuerySerializer(serializers.Serializer):
    chats = AgentChatSerializer(many=True)
    has_file_context = serializers.BooleanField(default=False)
