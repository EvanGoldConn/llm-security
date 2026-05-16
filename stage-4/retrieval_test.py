



# Tests retrieval ranking across multiple query phrasings without calling the LLM
# Use this to measure how reliably a chunk surfaces before and after poisoning

import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

DB_DIR = "/Volumes/UTM_DRIVE/llm-security/stage-4/db"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3 # number of top chunks (close vector distance) returned to be passed to LLM 


QUERY_PHRASINGS = [
    "What approvals do I need for a $3000 purchase?",
    "How do I get director approval for a purchase?",
    "What is the purchase approval process?",
    "How do I submit a purchase request?",
    "Who approves purchases over $500?",
    "What is the process for getting a purchase approved?",
]


def run_retrieval_test():
    # run the query through the embedding model, send those vectors to the chromaDB and have it return the top K closest vectors and have it return documents/metadata/distances.. then you iterate through those 3 results and get the source/distance/snippet and print them out
    print("Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection("bluetree_kb")

    for query in QUERY_PHRASINGS:
        print("\n" + "="*60)
        print("Query: " + query)

        
        query_embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"]
        )

        for i in range(len(results["documents"][0])):
            source = results["metadatas"][0][i]["source"]
            distance = str(round(results["distances"][0][i], 4))
            snippet = results["documents"][0][i][:80]
            rank = str(i + 1)
            print("  [" + rank + "] " + source + " (distance: " + distance + ")")
            print("       " + snippet + "...")


if __name__ == "__main__":
    run_retrieval_test()