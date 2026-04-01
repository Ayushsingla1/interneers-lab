from rest_framework.fields import ValidationError
from rest_framework.response import Response
from product_rag.domain.custom_exceptions import InvalidChatHistory, RAGRepositoryError
from ..application.service import RAGService
from rest_framework.viewsets import ViewSet
from .serializer import UploadSerializer, ChatListSerializer
from rest_framework import status


class RAGController(ViewSet):
    service: RAGService = None

    def upload(self, request):
        serialized_data = UploadSerializer(data=request.data)

        try:
            serialized_data.is_valid(raise_exception=True)
            file = serialized_data.validated_data["file"]
            self.service.upload(file)
            return Response(
                data="file uploaded successfully", status=status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response(
                data=f"data validation failed {str(e)}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                data=f"Error while uploading {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def query(self, request):
        serialized_data = ChatListSerializer(data=request.data)
        try:
            serialized_data.is_valid(raise_exception=True)
            response = self.service.query(serialized_data.validated_data["chats"])
            return Response(data=response, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                data=f"data validation failed {str(e)}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except InvalidChatHistory as e:
            return Repsonse(data=e, status=status.HTTP_400_BAD_REQUEST)

        except RAGRepositoryError as e:
            return Response(data=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(
                data=f"Error while querying {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
