# Local RAG System for Wyrd Media Labs Wiki
## Overview

I built a local Retrieval-Augmented Generation (RAG) system that answers questions about the Wyrd Media Labs company wiki. The system ingests exported Markdown documents from the wiki, converts them into vector embeddings, stores them in a local vector database, retrieves the most relevant sections for a query, and uses a local language model to generate answers grounded in the retrieved context.

The system runs fully locally using open-source tools, avoiding per-query API costs.

## Architecture

The system has four main stages:

1. Document Ingestion

    The wiki was exported as Markdown files.
    A Python script recursively loads all .md files from the exported folder.
    
    Each document is processed and prepared for chunking.

2. Chunking Strategy

I split documents based on Markdown headers (#, ##, ###).

Reasoning:

Wiki content is already structured using headings.

Each section typically represents a coherent idea or topic.

Chunking at headers preserves semantic structure better than fixed-length chunking.

Very small sections (<50 characters) are ignored to avoid embedding noise.

Each chunk stores metadata including:

source file path

section content

This allows traceability back to the original document.

3. Embedding and Vector Storage

Each chunk is converted into an embedding using the nomic-embed-text model via Ollama.

Reasons for this choice:

Lightweight

Runs locally

Designed for semantic search tasks

Embeddings are stored in ChromaDB, a simple local vector database.

Chroma allows:

fast similarity search

simple setup without external infrastructure

local persistence

4. Retrieval + Generation

When a user asks a question:

The query is embedded using the same embedding model.

ChromaDB performs vector similarity search to retrieve the most relevant chunks.

The retrieved chunks are combined into a context block.

A local LLM (Phi-3 via Ollama) generates the final answer using the retrieved context.

The model is prompted to answer only using the provided context to reduce hallucination.

## Design Decisions
Local Models

All models run locally using Ollama to meet the requirement that the system should not incur per-query costs.

Header-Based Chunking

Wiki pages already have hierarchical structure.
Chunking by headers keeps information grouped in meaningful sections.

This improves retrieval accuracy compared to arbitrary token splitting.

Simple Vector Database

ChromaDB was selected because:

easy setup

no server required

suitable for small to medium document sets

## Limitations

The system has several limitations:

1. No Reranking

Retrieved chunks are based purely on embedding similarity.
A reranking model could improve answer quality.

2. No Hybrid Search

The system only uses vector search.

Combining:

keyword search (BM25)

vector search

would improve retrieval for exact terms.

3. Chunk Size Variability

Header-based chunking can produce chunks of uneven size.

Very long sections could exceed optimal context length.

4. Latency

Because inference runs locally on CPU, generation is slower compared to cloud-based models.

5. No Evaluation Pipeline

There is currently no automated evaluation for answer accuracy or retrieval quality.

## Potential Improvements

If this system were expanded, the following improvements would be implemented:

Add Hybrid Retrieval

Combine:

vector search

keyword search

to improve recall.

Add Reranking

Use a cross-encoder model to rerank retrieved chunks before passing them to the LLM.

Improve Chunking

Implement token-based chunking with overlap to ensure important information is not split across chunks.

Add Source Citations

Return the original document source along with the generated answer.

Persistent Indexing

Currently the system re-indexes documents each time it runs.
Persisting the vector database would improve startup time.

## Where It Breaks

The system can fail in several scenarios:

Questions requiring reasoning across multiple documents.

Queries that use terminology not present in the documents.

Very long sections where important information is buried inside large chunks.

Ambiguous queries that retrieve irrelevant context.
