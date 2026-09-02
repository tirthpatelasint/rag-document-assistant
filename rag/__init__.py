"""RAG Module Package."""

from rag.loader import load_and_split_pdf, get_file_metadata
from rag.embeddings import get_embedding_model
from rag.retriever import (
    build_faiss_vector_store,
    build_bm25_retriever,
    build_hybrid_retriever,
    BM25Retriever,
    HybridRetriever,
    retrieve_with_details,
)
from rag.generator import generate_grounded_answer, get_groq_client, get_available_models

__all__ = [
    "load_and_split_pdf",
    "get_file_metadata",
    "get_embedding_model",
    "build_faiss_vector_store",
    "build_bm25_retriever",
    "build_hybrid_retriever",
    "BM25Retriever",
    "HybridRetriever",
    "retrieve_with_details",
    "generate_grounded_answer",
    "get_groq_client",
    "get_available_models",
]
