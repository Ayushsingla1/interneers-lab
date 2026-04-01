from product_rag.application.service import RAGService
from product_rag.api.rag_views import RAGController
from product_rag.infrastructure.rag_repo import RAGRepository

repository = RAGRepository()
service = RAGService(repository)

upload_doc = RAGController.as_view({"post": "upload"}, service=service)

query_doc = RAGController.as_view({"post": "query"}, service=service)
