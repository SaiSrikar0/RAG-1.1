from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Replace with your actual Google API Key
GOOGLE_API_KEY = "AIzaSyDFh-jz0Mk2DyoZfgOKzaZWVpANNnW-CgM"

# Initialize the embedding model
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# Sample text to generate embeddings
sample_texts = ["Test embedding example", "Another sample sentence"]

# Generate embeddings
try:
    embeddings = embeddings_model.embed_documents(sample_texts)
    print("Embeddings Generated Successfully!")
    print(embeddings)  # Print the first embedding to verify
except Exception as e:
    print("Error generating embeddings:", e)
