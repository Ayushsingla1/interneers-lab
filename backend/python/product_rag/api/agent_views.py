from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.fields import ValidationError
from rest_framework import status

from product_rag.application.agent_service import AgentService
from product_rag.domain.custom_exceptions import (
    AgentError,
    InvalidChatHistory,
    RAGRepositoryError,
)
from .agent_serializer import AgentUploadSerializer, AgentQuerySerializer


class AgentController(ViewSet):
    service: AgentService = None

    def upload(self, request):
        """Upload a PDF document to be indexed in the vector store."""
        serialized_data = AgentUploadSerializer(data=request.data)

        try:
            serialized_data.is_valid(raise_exception=True)
            file = serialized_data.validated_data["file"]
            self.service.upload(file)
            return Response(
                data="File uploaded successfully", status=status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response(
                data=f"Data validation failed: {str(e)}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                data=f"Error while uploading: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def query(self, request):
        """Process a query through the ReAct agent.

        Accepts chat history and a flag indicating if a file was uploaded.
        The agent decides whether to query the DB, vector store, or both.
        """
        serialized_data = AgentQuerySerializer(data=request.data)

        try:
            serialized_data.is_valid(raise_exception=True)
            validated = serialized_data.validated_data

            response = self.service.query(
                prompt=validated["chats"],
                has_file_context=validated["has_file_context"],
            )

            return Response(
                data={
                    "answer": response.answer,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response(
                data=f"Data validation failed: {str(e)}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except InvalidChatHistory as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

        except (AgentError, RAGRepositoryError) as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(
                data=f"Error while querying agent: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
