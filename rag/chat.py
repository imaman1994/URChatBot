# chat.py — retrieval part of RAG
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from langchain_ollama import OllamaEmbeddings

load_dotenv()  # loads OPENAI_API_KEY from .env

# 1. Same embedding model as used during indexing
embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

# 2. Connect to the EXISTING collection (no new data is stored)
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
        url="http://localhost:6333",
        collection_name='learning_rag'
)

# 3. Take user input
user_query = input("Ask something: ")

# 4. Similarity search -> relevant chunks only
search_results = vector_db.similarity_search(query=user_query)

# 5. Build a context string with content + page number + file location
context = "\n\n\n".join(
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata['page_label']}\n"
    f"File Location: {result.metadata['source']}"
    for result in search_results
)

SYSTEM_PROMPT = f"""
You are a helpful AI assistant who answers the user's query based on the
available context retrieved from a PDF file, along with page contents and
page numbers.

You should only answer the user based on the following context and guide
them to open the right page number to learn more.

Context:
{context}
"""

# 6. Send system prompt + user query to the chat model
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
response = client.chat.completions.create(
    model="llama3.2:1b",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ],
)

print(f"🤖: {response.choices[0].message.content}")
