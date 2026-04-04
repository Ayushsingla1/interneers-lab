import streamlit as st
import requests
import pandas as pd
from urllib.parse import quote

BACKEND_URL = "http://localhost:8000"
PRODUCT_URL = f"{BACKEND_URL}/products/"
CATEGORY_URL = f"{BACKEND_URL}/categories/"
QUERY_URL = f"{BACKEND_URL}/query/"

if "current_cursor" not in st.session_state:
    st.session_state.current_cursor = None

if "prev_stack" not in st.session_state:
    st.session_state.prev_stack = []

if "category" not in st.session_state:
    st.session_state.category = None

if "query" not in st.session_state:
    st.session_state.query = ""

if "mode" not in st.session_state:
    st.session_state.mode = "browse"  # browse | search

if "last_category" not in st.session_state:
    st.session_state.last_category = None

if "similar_query" in st.session_state:
    st.session_state.query = st.session_state.similar_query
    del st.session_state.similar_query


@st.cache_data()
def get_categories():
    response = requests.get(CATEGORY_URL)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)["title"].tolist()
    return []


@st.cache_data()
def fetch_products(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


st.title("Product Inventory")

categories = get_categories()

st.text_input("Search", key="query")

st.sidebar.selectbox(
    "Category",
    categories,
    index=None,
    key="category",
    placeholder="Choose the Category...",
)

if st.button("Search"):
    if len(st.session_state.query) > 3:
        st.session_state.mode = "search"
        st.session_state.current_cursor = None
        st.session_state.prev_stack = []

if st.session_state.mode == "search":
    if st.button("Clear Search"):
        st.session_state.mode = "browse"
        st.session_state.pop("query", None)
        st.rerun()


if st.session_state.category != st.session_state.last_category:
    st.session_state.current_cursor = None
    st.session_state.prev_stack = []
    st.session_state.last_category = st.session_state.category


def build_url():
    if st.session_state.mode == "search":
        return QUERY_URL + f"?q={quote(st.session_state.query)}"

    url = PRODUCT_URL
    params = []

    if st.session_state.current_cursor:
        params.append(f"cursor={st.session_state.current_cursor}")

    if st.session_state.category:
        params.append(f"category={quote(st.session_state.category)}")

    if params:
        url += "?" + "&".join(params)

    return url


url = build_url()
json_response = fetch_products(url)


if json_response:
    data = json_response["data"]

    if st.session_state.mode == "search":
        st.info(f"Showing similar products for: {st.session_state.query[:80]}...")

    for i, product in enumerate(data):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"**{product['name']}**")
            st.write(f"Description: {product['description'][:120]}...")
            st.write(f"Price: ₹{product['price']}")
            st.write(f"Quantity: {product['quantity']}")
            st.write(f"Category: {product['category']}")

        with col2:
            if st.button("Find Similar", key=f"similar_{i}"):
                st.session_state.similar_query = product["description"]
                st.session_state.mode = "search"
                st.session_state.current_cursor = None
                st.session_state.prev_stack = []
                st.rerun()

        st.divider()

    if st.session_state.mode == "browse":
        next_cursor = json_response.get("next_cursor")
        has_more = json_response.get("has_more", False)

        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.prev_stack or st.session_state.current_cursor:
                if st.button("Prev"):
                    if st.session_state.prev_stack:
                        st.session_state.current_cursor = (
                            st.session_state.prev_stack.pop()
                        )
                    else:
                        st.session_state.current_cursor = None
                    st.rerun()

        with col2:
            if has_more:
                if st.button("Next"):
                    if st.session_state.current_cursor:
                        st.session_state.prev_stack.append(
                            st.session_state.current_cursor
                        )
                    st.session_state.current_cursor = next_cursor
                    st.rerun()

if categories:
    with st.form("Add Product Form"):
        st.subheader("Add Product")

        product_name = st.text_input("Name", max_chars=50)
        product_description = st.text_input("Description", max_chars=200)
        product_brand = st.text_input("Brand", max_chars=50)
        product_price = st.number_input("Price", min_value=0)
        product_quantity = st.number_input("Quantity", min_value=0)
        product_category = st.selectbox("Category", categories)

        submitted = st.form_submit_button("Submit")

        if submitted:
            request_json = {
                "name": product_name,
                "description": product_description,
                "brand": product_brand,
                "price": product_price,
                "quantity": product_quantity,
                "category": product_category,
            }

            response = requests.post(url=f"{BACKEND_URL}/products/", json=request_json)

            if response.status_code == 201:
                st.success("Successfully added product")
            else:
                st.error("Unable to add product")
