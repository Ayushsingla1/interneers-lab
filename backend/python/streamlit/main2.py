import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/doc"

# ---------------------------
# SESSION STATE
# ---------------------------
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------
# FILE UPLOAD
# ---------------------------
if not st.session_state.uploaded:

    st.title("📄 Upload Document")

    uploaded_file = st.file_uploader("Upload the file you want to query about")

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
                    st.rerun()
                else:
                    st.error("Upload failed")


# ---------------------------
# CHAT UI
# ---------------------------
else:
    st.title("💬 Document Chat")

    # 🔁 Reset option
    if st.button("🔄 Upload New File"):
        st.session_state.uploaded = False
        st.session_state.chat_history = []
        st.rerun()

    # ---------------------------
    # SCROLLABLE CHAT AREA
    # ---------------------------
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["text"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["text"])

    # ---------------------------
    # FIXED INPUT (AUTO)
    # ---------------------------
    query = st.chat_input("Ask something about your document...")

    if query:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "text": query})

        # Show user message instantly
        with st.chat_message("user"):
            st.write(query)

        # Fetch response
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/query/", json={"chats": st.session_state.chat_history}
            )

        if response.status_code == 200:
            json_response = response.json()
            answer = json_response
        else:
            answer = "Error fetching response"

        # Add AI response
        st.session_state.chat_history.append({"role": "ai", "text": answer})

        # Show AI response
        with st.chat_message("assistant"):
            st.write(answer)
