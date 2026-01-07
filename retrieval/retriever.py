import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

collection = chroma_client.get_collection(name="learnloop_docs")

def embed_query(query: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-004",
        input=query
    )
    return response.data[0].embedding

def retrieve_embeddings(query: str, k: int = 5) -> list[str]:
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]
