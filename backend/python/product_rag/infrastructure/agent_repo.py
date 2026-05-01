from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable
from dotenv import load_dotenv
import requests

from product_rag.application.ports.outbound.agent_repo_ports import AgentRepoPorts
from product_rag.domain.entities.agent import AgentMessage, AgentResponse, AgentRole
from product_rag.domain.custom_exceptions import AgentError
from product_rag.infrastructure.agent_prompt import AGENT_SYSTEM_PROMPT
from product_rag.infrastructure.agent_tools import (
    get_products_by_date,
    get_products_by_category,
    create_vector_search_tool,
)
from product_rag.infrastructure.rag_repo import RAGRepository

load_dotenv()

BACKEND_URL = "http://localhost:8000"


class AgentRepository(AgentRepoPorts):

    def __init__(self, rag_repository: RAGRepository):
        self.rag_repository = rag_repository
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

        self.vector_search_tool = create_vector_search_tool(rag_repository)

        self.tools = [
            get_products_by_date,
            get_products_by_category,
            self.vector_search_tool,
        ]

        self.agent = None
        self._categories_loaded = False

    def _build_agent(self):
        """Build (or rebuild) the agent with current categories from the DB."""
        categories = self._fetch_categories()
        system_prompt = AGENT_SYSTEM_PROMPT.format(categories=categories)
        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=system_prompt,
        )

    @staticmethod
    def _fetch_categories() -> str:
        """Fetch available categories from the product API."""
        try:
            response = requests.get(f"{BACKEND_URL}/categories/")
            if response.status_code == 200:
                titles = [cat["title"] for cat in response.json().get("data", [])]
                return "\n".join(f"- {title}" for title in titles)
        except Exception:
            pass
        return "- (unable to load categories)"

    def upload_document(self, file_path: str) -> None:
        """Delegate document upload to the existing RAG repository."""
        content = self.rag_repository.load_document(file_path)
        chunks = self.rag_repository.text_splitter(content, 0, 500)
        self.rag_repository.save_chunks(chunks)

    @traceable
    def invoke_agent(
        self,
        chat_history: List[AgentMessage],
        has_file_context: bool,
    ) -> AgentResponse:
        """Run the ReAct agent with the given chat history."""

        if not self._categories_loaded:
            self._build_agent()
            self._categories_loaded = True

        try:
            messages = []
            for msg in chat_history[:-1]:
                if msg.role == AgentRole.USER:
                    messages.append(HumanMessage(content=msg.text))
                else:
                    messages.append(AIMessage(content=msg.text))

            latest_message = chat_history[-1].text
            if has_file_context:
                latest_message = (
                    f"[Note: A document has been uploaded to the system. "
                    f"Consider searching it if relevant.]\n\n{latest_message}"
                )
            messages.append(HumanMessage(content=latest_message))

            result = self.agent.invoke({"messages": messages})

            final_message = result["messages"][-1]
            tools_used = []
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tools_used.append(tc["name"])

            answer = final_message.content

            if isinstance(answer, list) and answer[0]:
                answer = answer[0]["text"]

            return AgentResponse(
                answer=answer,
                tools_used=tools_used,
            )

        except Exception as e:
            raise AgentError(f"Agent execution failed: {str(e)}")
