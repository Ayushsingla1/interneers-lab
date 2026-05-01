from product_rag.domain.custom_exceptions import InvalidChatHistory
from product_rag.domain.entities.agent import AgentMessage, AgentResponse, AgentRole
from product_rag.application.ports.inbound.agent_service_ports import AgentServicePorts
from product_rag.application.ports.outbound.agent_repo_ports import AgentRepoPorts
import tempfile
from langsmith import traceable


class AgentService(AgentServicePorts):

    def __init__(self, repo: AgentRepoPorts):
        self.repository = repo

    def upload(self, file) -> None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        self.repository.upload_document(tmp_path)

    @traceable
    def query(self, prompt: list, has_file_context: bool) -> AgentResponse:

        if len(prompt) == 0:
            raise InvalidChatHistory("No chats in history")
        elif prompt[-1]["role"] != "user":
            raise InvalidChatHistory("Latest message must be from user")

        chat_history = [
            AgentMessage(text=msg["text"], role=AgentRole(msg["role"]))
            for msg in prompt
        ]

        response = self.repository.invoke_agent(
            chat_history=chat_history,
            has_file_context=has_file_context,
        )

        return response
