import pandas as pd
import requests
import streamlit as st
from urllib.parse import quote

st.title("Product Inventory")

url = "http://localhost:8000"
page = 1
limit = 10
category = ""

response = requests.get(f"{url}/categories/")

categories = None
categories_to_categories_id = {}
d = {}

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    d = df.set_index("title")['id'].to_dict()
    categories_to_categories_id = d
    categories = df['title']
    category = st.sidebar.selectbox(
        "Category of product you want : ",
        categories,
        index=None,
        placeholder="Choose the Category...",
    )

product_url = f"{url}/products/?page={page}&limit={limit}" 

if category:
    product_url = product_url + f"&category={quote(category)}"

response = requests.get(product_url)
if response.status_code == 200:
    data = response.json()
    dataframe = pd.DataFrame(data, columns=['name', 'description', 'price', 'quantity'])
    dataframe['stock_level'] = dataframe['quantity'].apply(lambda x : "Normal" if x >= 100  else "Low")
    st.dataframe(dataframe)
else:
    print(response.json())
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
    print(clicked)

    request_json = {
        "name": product_name,
        "description": product_description,
        "brand": product_brand,
        "price": product_price,
        "quantity": product_quantity,
        "category": d[product_category]
    }

    print(request_json)

    if clicked:
        print(d[product_category]) 
        response = requests.post(
            url=f"{url}/products/",
            json=request_json
        )
        print(response)

        if response.status_code == 201:
            st.success("Successfully added product")
        else:
            st.error("Unable to add product")

st.toast("Data loaded successfully")