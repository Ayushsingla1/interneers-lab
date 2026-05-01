from product_rag.application.agent_service import AgentService
from product_rag.api.agent_views import AgentController
from product_rag.infrastructure.rag_repo import RAGRepository
from product_rag.infrastructure.agent_repo import AgentRepository

repository = RAGRepository()

# ─── Agent wiring ────────────────────────────────────────────────────────────
# Reuses the same RAGRepository instance for vector search capabilities

agent_repository = AgentRepository(rag_repository=repository)
agent_service = AgentService(agent_repository)

agent_upload = AgentController.as_view({"post": "upload"}, service=agent_service)
agent_query = AgentController.as_view({"post": "query"}, service=agent_service)
