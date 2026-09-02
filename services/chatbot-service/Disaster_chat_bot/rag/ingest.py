from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from ..config import GOOGLE_GEMINI_KEY

loader = PyPDFLoader(
    "rag/documents/wildfire_doc.pdf"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GOOGLE_GEMINI_KEY
)

Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="rag/chroma_db"  
)
print("done")