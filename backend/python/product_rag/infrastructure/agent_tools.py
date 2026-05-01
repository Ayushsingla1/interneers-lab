from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List
import requests
from urllib.parse import quote
from product_rag.domain.entities.chat import Chat, ROLE

BACKEND_URL = "http://localhost:8000"


class GetProductsByDateInput(BaseModel):
    date: str = Field(
        description="The date to fetch products added after. Must be in dd-mm-yyyy format. "
        "Month is 1-indexed starting from January."
    )
    category: Optional[str] = Field(
        default=None, description="Optional category filter to narrow down results."
    )


class GetProductsByCategoryInput(BaseModel):
    category: str = Field(
        description="The category name to filter products by (e.g., 'Electronics', 'Toys')."
    )


class SearchVectorStoreInput(BaseModel):
    query: str = Field(
        description="The search query to find relevant content from uploaded documents. "
        "Should be a natural language question or topic."
    )


@tool(args_schema=GetProductsByDateInput)
def get_products_by_date(date: str, category: Optional[str] = None) -> dict:
    """Fetch products from the database that were added after a specific date.
    Optionally filter by category. Returns product list and whether more exist.
    Use this when the user asks about products added after a certain date."""

    url = f"{BACKEND_URL}/products/?after={date.strip()}"
    if category is not None and category.strip() != "":
        url += f"&category={quote(category.strip())}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            return {
                "products": response_json["data"],
                "has_more": response_json.get("has_more", False),
            }
        else:
            return {
                "error": f"Failed to fetch products. Status: {response.status_code}"
            }
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@tool(args_schema=GetProductsByCategoryInput)
def get_products_by_category(category: str) -> dict:
    """Fetch products from the database filtered by a specific category.
    Returns product list and whether more exist.
    Use this when the user asks about products in a certain category."""

    url = f"{BACKEND_URL}/products/?category={quote(category.strip())}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            return {
                "products": response_json["data"],
                "has_more": response_json.get("has_more", False),
            }
        else:
            return {
                "error": f"Failed to fetch products. Status: {response.status_code}"
            }
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def create_vector_search_tool(rag_repository):
    """Factory that creates a vector search tool bound to a specific RAG repository instance."""

    @tool(args_schema=SearchVectorStoreInput)
    def search_uploaded_documents(query: str) -> str:
        """Search through uploaded PDF documents for relevant content.
        Use this when the user asks about content from uploaded files/documents,
        or when the query seems to require information from external documents
        rather than the product database.
        Returns relevant text chunks from the uploaded documents."""

        chat_history = [Chat(text=query, role=ROLE.USER)]

        try:
            chunks = rag_repository.retrieve_relevant_chunks(chat_history=chat_history)
            if not chunks:
                return "No relevant content found in the uploaded documents."

            formatted = "\n\n".join(
                f"--- Chunk {i+1} ---\n{chunk}" for i, chunk in enumerate(chunks)
            )
            return f"Found {len(chunks)} relevant sections from uploaded documents:\n\n{formatted}"
        except Exception as e:
            return f"Error searching documents: {str(e)}"

    return search_uploaded_documents
