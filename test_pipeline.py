"""Automated End-to-End Pipeline Test."""

import os
import sys

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from rag import (
    load_and_split_pdf,
    get_embedding_model,
    build_faiss_vector_store,
    build_bm25_retriever,
    retrieve_with_details,
    generate_grounded_answer,
)
from ui.components import get_chat_download_data


def run_pipeline_test():
    print("=" * 60)
    print("RUNNING END-TO-END RAG PIPELINE VERIFICATION")
    print("=" * 60)

    pdf_path = os.path.join("data", "documents", "Leave Policy 1.0.pdf")
    if not os.path.exists(pdf_path):
        print(f"Error: Sample PDF not found at {pdf_path}")
        return

    # 1. Load PDF
    raw_docs, chunks, meta = load_and_split_pdf(pdf_path)
    print("1. PDF Loaded successfully:")
    print(f"   - Filename: {meta['filename']}")
    print(f"   - Total Pages: {meta['total_pages']}")
    print(f"   - Total Chunks: {meta['chunk_count']}")
    print(f"   - Size: {meta['size_formatted']}")

    # 2. Embedding & Vector DB
    emb = get_embedding_model()
    vs = build_faiss_vector_store(chunks, emb)
    vr = vs.as_retriever(search_kwargs={"k": 5})
    print("2. FAISS Vector Store built with HuggingFace embeddings.")

    # 3. BM25 Retriever
    bm = build_bm25_retriever(chunks, k=5)
    print("3. BM25 Okapi index built successfully.")

    # 4. Test Query
    query = "What is the sick leave policy?"
    print("\n" + "-" * 50)
    print(f"Query: {query}")
    details = retrieve_with_details(query, vr, bm, k=5, rrf_k=60)
    print(f"Retrieved {len(details['top_chunks'])} chunks via Hybrid RRF.")

    gen = generate_grounded_answer(query, details["top_chunks"])
    print(f"Answer:\n{gen['answer']}")
    print(f"Sources returned: {len(gen['sources'])}")

    print("\n" + "=" * 60)
    print(">>> PIPELINE VERIFICATION COMPLETE! <<<")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline_test()
