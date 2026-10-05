from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings


load_dotenv()

pdf_path = Path(__file__).parent / "ai.pdf"

# Load file into the python program
loader = PyPDFLoader(pdf_path)
doc = loader.load()

print(doc[12])

# Splitting text into chunks

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)


chunks = text_splitter.split_documents(documents=doc)

# Vector Embedding of above chunks

embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name='learning_rag'
)

print("Indexing of pdf phase is done...")