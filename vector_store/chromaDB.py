import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from typing import List


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

collection = chroma_client.get_or_create_collection(
    name="learnloop_docs"
)

def embed_chunks(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        response = client.embeddings.create(
            model="text-embedding-004",
            input=batch
        )

        embeddings.extend([item.embedding for item in response.data])

    return embeddings



def store_chunks(chunks: list[str]):
    embeddings = embed_chunks(chunks)

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
    
    print(f"Stored {len(chunks)} chunks in Chroma")
