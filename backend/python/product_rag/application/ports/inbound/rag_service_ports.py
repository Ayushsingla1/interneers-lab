from abc import ABC, abstractmethod


class RAGServicePorts(ABC):
    @abstractmethod
    def upload(self, file):
        pass

    @abstractmethod
    def query(self, prompt) -> str:
        pass
