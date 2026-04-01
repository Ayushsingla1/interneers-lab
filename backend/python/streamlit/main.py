import pandas as pd
import requests
import streamlit as st
from urllib.parse import quote

st.title("Product Inventory")

url = "http://localhost:8000"

if "page" not in st.session_state:
    st.session_state.page = 1
if "limit" not in st.session_state:
    st.session_state.limit = 10


page = st.session_state.page
limit = st.session_state.limit
category = ""

response = requests.get(f"{url}/categories/")

categories = None

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    categories = df["title"]
    category = st.sidebar.selectbox(
        "Category of product you want : ",
        categories,
        index=None,
        placeholder="Choose the Category...",
    )

product_url = f"{url}/products/?page={page}&limit={limit}"
query_url = f"{url}/query/"

search_text = st.text_input("Search", placeholder="Search products")

if st.button("Search"):
    if search_text.strip():
        st.session_state.query_params = search_text
        st.session_state.page = 1
    else:
        st.session_state.pop("query_params", None)
    st.rerun()

if category:
    product_url = product_url + f"&category={quote(category)}"

next_page = None

request_url = product_url

if "query_params" in st.session_state:
    request_url = f"{query_url}?q={st.session_state.query_params}"

response = requests.get(request_url)

if response.status_code == 200:
    data = response.json()
    dataframe = pd.DataFrame(data, columns=["name", "description", "price", "quantity"])
    dataframe["stock_level"] = dataframe["quantity"].apply(
        lambda x: "Normal" if x >= 100 else "Low"
    )

    print(dataframe)
    for idx, row in dataframe.iterrows():

        col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 1, 1, 1, 2])
        col1.write(row["name"])
        col2.write(row["description"])
        col3.write(row["price"])
        col4.write(str(row["quantity"]))
        col5.write(row["stock_level"])

        if col6.button("Similar", key=f"similar_{idx}"):
            print(row["name"], " ", row["description"])
            st.session_state.query_params = row["description"]
            st.session_state.page = 1
            st.rerun()

        col1, col2 = st.columns(2, gap="small")

    with col1:
        if len(data) != 0:
            next_page = st.button("Next")
            if next_page:
                st.session_state.page = st.session_state.page + 1
                st.rerun()
    with col2:
        if st.session_state.page > 1:
            prev_page = st.button("Prev")
            if prev_page:
                st.session_state.page = st.session_state.page - 1
                st.rerun()

else:
    st.error("Unable to fetch data")

if categories is not None:
    form1 = st.form("Add Product Form")
    product_name = form1.text_input("Name", max_chars=50)
    product_description = form1.text_input("Description", max_chars=200)
    product_brand = form1.text_input("Brand", max_chars=50)
    product_price = form1.number_input("Price", min_value=0)
    product_quantity = form1.number_input("Quantity", min_value=0)
    product_category = form1.selectbox("Category", categories)

    clicked = form1.form_submit_button("Submit")

    request_json = {
        "name": product_name,
        "description": product_description,
        "brand": product_brand,
        "price": product_price,
        "quantity": product_quantity,
        "category": product_category,
    }

    if clicked:
        response = requests.post(url=f"{url}/products/", json=request_json)
        print(response)

        if response.status_code == 201:
            st.success("Successfully added product")
        else:
            st.error("Unable to add product")

st.toast("Data loaded successfully")
