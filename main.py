from ingest import load_markdown_docs, chunk_documents
from rag import index_chunks, retrieve, generate_answer

# 1. Load
docs = load_markdown_docs("doc")

# 2. Chunk
chunks = chunk_documents(docs)

# 3. Index
index_chunks(chunks)

print(f"Indexed {len(chunks)} chunks.")

# 4. Ask questions loop
while True:
    query = input("\nAsk a question (or type exit): ")

    if query.lower() == "exit":
        break

    context = retrieve(query)
    answer = generate_answer(query, context)

    print("\nAnswer:\n")
    print(answer)
