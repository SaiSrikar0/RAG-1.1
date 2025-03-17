from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATA_PATH = "data/sample_data.jsonl"
api_key = "AIzaSyDFh-jz0Mk2DyoZfgOKzaZWVpANNnW-CgM"  # Corrected this line

def get_vector_store():
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        docs = [json.loads(line) for line in f]

    texts = [doc["text"] for doc in docs if "text" in doc]

    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=api_key, model="models/embedding-001")
    if not texts:
        raise ValueError("No texts were loaded for indexing. Check your data file.")
    vector_store = FAISS.from_texts(texts, embeddings)

    return vector_store