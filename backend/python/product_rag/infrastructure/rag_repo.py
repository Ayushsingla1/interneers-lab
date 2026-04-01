from product_rag.domain.custom_exceptions import RAGRepositoryError
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

    def get_llm_response(self, query: str, chunks: List[str]) -> str:
        prompt = f""" Respond to the user query based on the data given to you. 
       If data given doesn't contain any related information about the query just say : 
       "The document does not contain any information regarding this topic" rather than
       giving answers by yourself.
       data : {" ".join(chunks)}
       user query : {query}
       """
        try:
            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            raise RAGRepositoryError(
                f"Unexcpected error while generating the response. {str(e)}"
            )
