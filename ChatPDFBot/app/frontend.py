import streamlit as st
import requests

st.title("ChatPDFBot 🤖")
# Uncomment the following line to use in docker
BACKEND_URL = "http://backend:8000"

# Uncomment the following line to use a local backend
# BACKEND_URL = "http://localhost:8000"

# Initialize session state variables
if 'reset' not in st.session_state:
    st.session_state.reset = False
    st.session_state.chat_history = []
    st.session_state.pdf_uploaded = False

# New Chat button - triggers reset
if st.sidebar.button("New Chat"):
    st.session_state.reset = True
    st.rerun()

# Handle reset
if st.session_state.reset:
    st.session_state.chat_history = []
    st.session_state.pdf_uploaded = False
    st.session_state.reset = False
    # Clear the file uploader by using a unique key based on reset count
    if 'upload_key' not in st.session_state:
        st.session_state.upload_key = 0
    st.session_state.upload_key += 1

# File uploader with dynamic key
pdf_file = st.file_uploader("Upload a PDF", 
                          type="pdf", 
                          key=f"upload_pdf_{st.session_state.upload_key if 'upload_key' in st.session_state else 0}")

if pdf_file:
    try:
        response = requests.post(
            f"{BACKEND_URL}/upload",
            files={"file": (pdf_file.name, pdf_file)}
        )
        if response.status_code == 200:
            st.success(f"**Uploaded:** {pdf_file.name}")
            st.session_state.pdf_uploaded = True
            st.info("Now you can ask any query related to the content of the PDF!")
        else:
            st.error(f"Upload failed: {response.text}")
    except Exception as e:
        st.error(f"Upload error: {str(e)}")

# Chat interface
user_input = st.chat_input("Ask something...")

if user_input:
    try:
        payload = {"query": user_input}
        if pdf_file:
            payload["filename"] = pdf_file.name

        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response_data = response.json()
        if response.status_code == 200 and "response" in response_data:
            ai_response = response_data["response"]
        else:
            ai_response = "💬 Hi, I'm ChatPDF Bot!"

        if not pdf_file:
            ai_response += "\n\n Please **upload** your **PDF** file and feel free to ask any **query** based on its content."

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("ai", ai_response))

        if len(st.session_state.chat_history) > 10:
            st.session_state.chat_history = st.session_state.chat_history[-10:]

    except requests.exceptions.Timeout:
        st.error("Request timed out. Try a shorter or simpler question.")
    except Exception as e:
        st.error(f"Connection error: {str(e)}")

# Display chat history
for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("assistant"):
            st.markdown(message)