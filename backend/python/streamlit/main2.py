import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/doc/agent"

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.header("Document Upload")
    st.caption(
        "Upload a PDF to let the agent search its content alongside the product database."
    )

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file:
        if st.button("Upload"):
            with st.spinner("Uploading..."):
                files = {
                    "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                response = requests.post(f"{BACKEND_URL}/upload/", files=files)

                if response.status_code == 200:
                    st.success("Uploaded successfully!")
                    st.session_state.uploaded = True
                else:
                    st.error("Upload failed")

    if st.session_state.uploaded:
        st.info("Document loaded — the agent can search it.")

    if st.button("clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["text"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["text"])

query = st.chat_input(
    "Ask about products, categories, dates, or your uploaded document..."
)

if query:
    st.session_state.chat_history.append({"role": "user", "text": query})

    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Thinking..."):
        payload = {
            "chats": st.session_state.chat_history,
            "has_file_context": st.session_state.uploaded,
        }
        response = requests.post(f"{BACKEND_URL}/query/", json=payload)

    if response.status_code == 200:
        json_response = response.json()
        answer = json_response.get("answer", "No response from agent.")
    else:
        answer = "Error fetching response from agent."

    st.session_state.chat_history.append({"role": "ai", "text": answer})

    with st.chat_message("assistant"):
        st.write(answer)
