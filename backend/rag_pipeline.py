from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
from indexing import get_vector_store

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY missing")

def generate_answer(question: str):
    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=api_key, model="models/embedding-001")
    vector_store = get_vector_store()

    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.0-flash", temperature=0.7)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=False
    )

    result = qa_chain.run(question)
    return result