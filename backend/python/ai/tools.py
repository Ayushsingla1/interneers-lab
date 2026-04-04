from langchain.tools import tool
import requests
from response import generate
from urllib.parse import quote
from pydantic import BaseModel, Field
from pprint import pprint


class GetProductsInput(BaseModel):

    category: str | None = Field(
        default=None, description="Used to specify the category of products required"
    )

    date: str | None = Field(
        default=None,
        description="""Used to fetch products added after a specified date. Should be in dd-mm-yyyy format. Month should be indexed
        from 1 starting from january""",
    )


BACKEND_URL = "http://localhost:8000/products/"


@tool(args_schema=GetProductsInput)
def get_products(category: str | None, date: None | str):
    """Allow to fetch products from database. It also supports filter like category and date. The response contains
    products as well as a has_more attribute , if has_more is true it mean more products exists and you should tell the
    user that more products exist and you should visit the site for that, else if has_more is false just return the products nothing else.
    """

    print(category, " ", date)
    url = BACKEND_URL
    if category is not None and category.strip() != "":
        url += f"?category={quote(category.strip())}&"
    if date is not None and date.strip() != "":
        if url[-1] == "/":
            url += f"?after={date.strip()}"
        else:
            url += f"after={date.strip()}"

    response = requests.get(url)

    pprint(response)

    if response.status_code == 200:
        response_json = response.json()
        return {
            "products": response_json["data"],
            "has_more": response_json["has_more"],
        }
    else:
        return "Unable to fetch products"


@tool
def generate_products(scenario: str, count: int):
    """This tool is used to generate a list of products, provided the event and count of products required"""

    prompt = f"""Suppose you are a store manager and supposed to fill your inventory based on the following scenario : {scenario} .Generate data about 
    {count} products based on the schema given"""

    print("hi there")
    return generate(prompt)
