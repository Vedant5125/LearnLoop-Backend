from pipeline.build_chunks import get_all_chunks
from vector_store.chromaDB import store_chunks

if __name__ == "__main__":
    print("🚀 Starting data ingestion pipeline...")
    chunks = get_all_chunks()
    store_chunks(chunks)
    print("✨ Ingestion complete.")