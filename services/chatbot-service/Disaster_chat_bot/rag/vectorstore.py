from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_GEMINI_KEY

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GOOGLE_GEMINI_KEY
)

vectorstore = Chroma(
    persist_directory="rag/chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)