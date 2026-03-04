import os
import re

def load_markdown_docs(root_folder):
    documents = []

    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                documents.append({
                    "content": content,
                    "source": path
                })

    return documents


def split_by_headers(text):
    # Split at H1, H2, H3
    sections = re.split(r'\n(?=#+ )', text)
    return sections


def chunk_documents(documents):
    chunks = []

    for doc in documents:
        sections = split_by_headers(doc["content"])

        for section in sections:
            if len(section.strip()) < 50:
                continue

            chunks.append({
                "content": section.strip(),
                "source": doc["source"]
            })

    return chunks
