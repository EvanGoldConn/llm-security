





import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import ollama

load_dotenv()

DB_DIR = "/Volumes/UTM_DRIVE/llm-security/stage-4/db"
EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "qwen2.5:7b"
TOP_K = 3 #how many chunks ChomraDB returns from similarity search




def load_resources():
    model = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection("bluetree_kb")
    return model, collection

def retrieve_chunks(query, model, collection, top_k=TOP_K):
    """take a query string, embeds it using  model from load_resources()
     and searches ChromaDB for the top K closest chunks and returns them as a 
     list of dicts to be used in assembled_context_window()"""
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )#return the top K most similar chunks to the [encoded] user query
    #https://docs.trychroma.com/docs/querying-collections/query-and-get
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i] 
            #distance = how far apart 2 vectors are in embedding space
            #smaller distance = more similiarity, further = unsimilar
        })
    return chunks


def assemble_context_window(query, chunks):
    """ takes query string + chunks returned from retrieve_chunks, formats them 
    into a single lableed prompt string that the LLM reads"""
    context_blocks = []
    for chunk in chunks:
        distance_str = str(round(chunk["distance"], 4))
        block = "--- from " + chunk["source"] + " (distance: " + distance_str + ") ---\n" + chunk["text"]
        context_blocks.append(block)

    context_text = "\n\n".join(context_blocks)

    prompt = ("You are a helpful assistant for BlueTree Technologies. "
              "Answer the user's question based only on the context provided below. "
              "If the answer is not in the context, say you don't know.\n\n"
              "Context:\n" + context_text + "\n\nQuestion:\n" + query)

    return prompt


def query_rag(query, model, collection):
    """main orchestrator function, calls chunk retrieval & context window assembly functions, 
    then passes assembled prompt into the LLM. Only externally callable function"""
    chunks = retrieve_chunks(query, model, collection)
    prompt = assemble_context_window(query, chunks)

    print("\nQuery: " + query)
    print("\nRetrieved chunks:")
    for i, chunk in enumerate(chunks):
        distance_str = str(round(chunk["distance"], 4))
        print("  [" + str(i + 1) + "] " + chunk["source"] + " (distance: " + distance_str + ")")
        print("       " + chunk["text"][:80] + "...")

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"]
    print("\nResponse:\n" + answer)
    return answer, chunks


if __name__ == "__main__":
    print("Loading resources...")
    model, collection = load_resources()

    # test_queries = [
    #     "How many vacation days do employees get?",
    #     "What are the password requirements?",
    #     "How do I report a security incident?",
    #     "What approvals do I need for a $3000 purchase?"
    # ]

    test_queries = [
        "What approvals do I need for a $3000 purchase and how do I get the approval?"
    ]

    for query in test_queries:
        print("\n" + "="*60)
        query_rag(query, model, collection)