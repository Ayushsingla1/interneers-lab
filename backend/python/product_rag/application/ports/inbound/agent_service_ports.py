from abc import ABC, abstractmethod
from typing import List, Optional

from product_rag.domain.entities.agent import AgentResponse, AgentMessage


class AgentServicePorts(ABC):

    @abstractmethod
    def upload(self, file) -> None:
        pass

    @abstractmethod
    def query(self, prompt: list, has_file_context: bool) -> AgentResponse:
        pass
