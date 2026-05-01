from abc import ABC, abstractmethod
from typing import List, Optional

from product_rag.domain.entities.agent import AgentMessage, AgentResponse


class AgentRepoPorts(ABC):

    @abstractmethod
    def upload_document(self, file_path: str) -> None:
        pass

    @abstractmethod
    def invoke_agent(
        self,
        chat_history: List[AgentMessage],
        has_file_context: bool,
    ) -> AgentResponse:
        pass
