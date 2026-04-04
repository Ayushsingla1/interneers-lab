from product_rag.domain.custom_exceptions import RAGRepositoryError
from product_rag.domain.entities.chat import ChatHistory
from ..application.ports.outbound.rag_repo_ports import RAGRepoPorts
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_cohere import CohereEmbeddings
from typing import List
from dotenv import load_dotenv

load_dotenv()


class RAGRepository(RAGRepoPorts):

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
        self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
        self.vector_store = Chroma(
            collection_name="product", embedding_function=self.embeddings
        )

    def load_document(self, file_path) -> str:
        loader = PyPDFLoader(file_path=file_path, mode="single")
        docs = loader.load()
        return docs[0].page_content

    def text_splitter(
        self, text: str, overlap: int = 0, chunk_size: int = 1000
    ) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=overlap
        )
        chunks = splitter.split_text(text)
        return chunks

    def save_chunks(self, chunks: List[str]):
        try:
            self.vector_store.add_texts(chunks)
        except Exception as e:
            raise RAGRepositoryError(
                f"Unexcpected error while uploading to db. {str(e)}"
            )

    def retrieve_relevant_chunks(self, query: str, count: int = 3) -> List[str]:
        try:
            docs = self.vector_store.similarity_search(query, k=count)
            return [doc.page_content for doc in docs]
        except Exception as e:
            raise RAGRepositoryError(
                f"Unexcpected error while fetching from db. {str(e)}"
            )

    def get_llm_response(self, chat_history: ChatHistory, chunks: List[str]) -> str:
        system_prompt = """You are a precise document assistant. Your job is to answer user queries strictly based on the provided document context.

    Rules:
    - Answer ONLY from the provided context. Do not use prior knowledge.
    - If the context lacks relevant information, respond exactly: "The document does not contain any information regarding this topic."
    - Be concise and direct. Avoid filler phrases like "Based on the document..." or "According to the context...".
    - If the answer is partially available, provide what's found and clearly state what's missing.
    - Preserve technical terms, names, and numbers exactly as they appear in the context."""

        context = "\n".join(f"- {chunk}" for chunk in chunks)

        conversation = ""
        if chat_history:
            for message in chat_history[:-1]:
                role = "User" if message.role.value == "user" else "Assistant"
                conversation += f"{role}: {message.text}\n"

        latest_query = chat_history[-1].text if chat_history else ""

        prompt = f"""### Document Context:
    {context}

    ### Conversation History:
    {conversation.strip() if conversation else "No prior conversation."}

    ### Current User Query:
    {latest_query}

    ### Instructions:
    Answer the current query using only the document context above.
    If relevant, you may reference previous conversation turns for clarity."""

        try:
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = self.model.invoke(full_prompt)
            return response.content
        except Exception as e:
            raise RAGRepositoryError(
                f"Unexpected error while generating the response. {str(e)}"
            )
