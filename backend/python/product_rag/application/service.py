from product_rag.domain.custom_exceptions import InvalidChatHistory
from .ports.inbound.rag_service_ports import RAGServicePorts
from .ports.outbound.rag_repo_ports import RAGRepoPorts
import tempfile


class RAGService(RAGServicePorts):

    def __init__(self, repo: RAGRepoPorts):
        self.repository = repo

    def upload(self, file):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        content = self.repository.load_document(tmp_path)
        chunks = self.repository.text_splitter(content, 0, 1000)
        self.repository.save_chunks(chunks)

    def query(self, prompt) -> str:

        if len(prompt) == 0:
            raise InvalidChatHistory("No chats in history")
        elif prompt[len(prompt) - 1]["role"] != "user":
            raise InvalidChatHistory("Latest message must be from user")

        chunks = self.repository.retrieve_relevant_chunks(
            query=prompt[len(prompt) - 1]["text"]
        )
        llm_response = self.repository.get_llm_response(prompt, chunks)
        return llm_response
