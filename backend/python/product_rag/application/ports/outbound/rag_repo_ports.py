from abc import ABC, abstractmethod
from typing import List


class RAGRepoPorts(ABC):
    @abstractmethod
    def load_document(self, file_path) -> str:
        pass

    @abstractmethod
    def text_splitter(self, text: str, overlapp: int, length: int) -> List[str]:
        pass

    @abstractmethod
    def save_chunks(self, chunks: List[str]):
        pass

    @abstractmethod
    def retrieve_relevant_chunks(self, query: str, count: int = 3) -> List[str]:
        pass

    @abstractmethod
    def get_llm_response(self, query: str, chunks: List[str]) -> str:
        pass
