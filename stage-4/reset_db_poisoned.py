

# Wipes ChromaDB and reinjects from both data/documents/ and data/poisoned/
# Use this to practice vector DB poisoning with pre-staged poisoned documents

import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

DB_DIR = "/Volumes/UTM_DRIVE/llm-security/stage-4/db"
DOCS_DIR = "/Volumes/UTM_DRIVE/llm-security/stage-4/data/documents"
POISONED_DIR = "/Volumes/UTM_DRIVE/llm-security/stage-4/data/poisoned"
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


def ingest_directory(directory, collection, model):
    total_chunks = 0
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, "r") as f:
            text = f.read()

        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        source_name = filename.replace(".txt", "")

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = source_name + "_chunk_" + str(i)
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

        print("  " + filename + ": " + str(len(chunks)) + " chunks ingested")
        total_chunks += len(chunks)
    return total_chunks


def reset_with_poisoned():
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

    print("\nIngesting clean documents...")
    clean_count = ingest_directory(DOCS_DIR, collection, model)

    print("\nIngesting poisoned documents...")
    poisoned_count = ingest_directory(POISONED_DIR, collection, model)

    total = clean_count + poisoned_count
    print("\nReset complete. Total chunks stored: " + str(total))
    print("  Clean: " + str(clean_count) + " chunks")
    print("  Poisoned: " + str(poisoned_count) + " chunks")


if __name__ == "__main__":
    reset_with_poisoned()