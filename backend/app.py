import streamlit as st
import requests
import time

# Configure the page
st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for UI
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stButton > button {
        font-size: 18px;
        font-weight: bold;
        width: 100%;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 5px;
    }
    .status-online {
        background-color: #4CAF50;
    }
    .status-offline {
        background-color: #f44336;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🤖 Real-Time RAG Assistant</h1>", unsafe_allow_html=True)
st.markdown("---")

# Backend API URL (Update if deployed)
API_URL = "http://127.0.0.1:8000"

# Check API Status
def check_api_status():
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False

# Display API Status
api_status = check_api_status()
status_color = "status-online" if api_status else "status-offline"
status_text = "Online" if api_status else "Offline"
st.markdown(f"<span class='status-indicator {status_color}'></span> Backend Status: {status_text}", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.write("This is a Retrieval-Augmented Generation (RAG) assistant using FastAPI and OpenAI.")
    st.markdown("### 💡 Tips")
    st.write("- Be specific in your queries")
    st.write("- Use clear language")
    st.write("- If no response, check API status")
    st.markdown("### 🔧 Configuration")
    st.write(f"Backend URL: {API_URL}")

# User Input
query = st.text_area(
    "🔍 Ask a Question:",
    height=100,
    placeholder="Enter your question...",
    help="Press Ctrl+Enter or click 'Get Answer' to submit."
)

# Submit Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit_button = st.button("🔍 Get Answer", type="primary", use_container_width=True)

# Handle API Call
if submit_button or (query and len(query.strip()) > 0):
    if not api_status:
        st.error("⚠️ Backend is not available. Please ensure the FastAPI server is running.")
    elif query.strip():
        with st.spinner("🤔 Thinking..."):
            try:
                # Send a POST request to the /query endpoint
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": query.strip()},
                    timeout=30
                )

                if response.status_code == 200:
                    st.markdown("### 📝 Answer")
                    st.markdown(response.json().get("answer", "No response received."))
                else:
                    st.error(f"⚠️ Error: {response.json().get('detail', 'Unknown error')}")
                    st.error(f"Status Code: {response.status_code}")

            except requests.exceptions.Timeout:
                st.error("⏱️ The request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("📡 Could not connect to the backend. Ensure FastAPI is running.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid question.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666666; padding: 10px;'>
        Made by Raggers
    </div>
    """, 
    unsafe_allow_html=True
)