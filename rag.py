import chromadb
import ollama

client = chromadb.Client()
collection = client.create_collection("wiki")

def embed_text(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]


def index_chunks(chunks):
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk["content"])

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[{"source": chunk["source"]}]
        )

def retrieve(query, top_k=2):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are answering questions based ONLY on the context below.

Context:
{context}

Question:
{query}

Answer clearly and concisely:
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={"num_predict": 150}  # limit tokens
    )

    return response["message"]["content"]
