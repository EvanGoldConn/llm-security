import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

DOCS_DIR = "/Volumes/UTM_DRIVE/llm-security/stage-4/data/documents"
DB_DIR = "/Volumes/UTM_DRIVE/llm-security/stage-4/db"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80


def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def ingest_documents(docs_dir):
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)

    existing = [c.name for c in client.list_collections()]
    if "bluetree_kb" in existing:
        client.delete_collection("bluetree_kb")
        print("Existing collection deleted.")

    collection = client.create_collection("bluetree_kb")
    print("Collection created.")

    total_chunks = 0

    for filename in os.listdir(docs_dir):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(docs_dir, filename)
        with open(filepath, "r") as f:
            text = f.read()

        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        source_name = filename.replace(".txt", "")

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{source_name}_chunk_{i}"
            embedding = model.encode(chunk).tolist()

            ids.append(chunk_id)
            embeddings.append(embedding)
            documents.append(chunk)
            metadatas.append({"source": filename})

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        print(f"  {filename}: {len(chunks)} chunks ingested")
        total_chunks += len(chunks)

    print(f"\nIngestion complete. Total chunks stored: {total_chunks}")


if __name__ == "__main__":
    ingest_documents(DOCS_DIR)