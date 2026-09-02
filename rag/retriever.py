"""Retriever implementations: FAISS Vector Store, BM25 Keyword Search, and Hybrid RRF."""

from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from rank_bm25 import BM25Okapi
from pydantic import Field


class BM25Retriever(BaseRetriever):
    """BM25 Keyword Retriever matching exact token matches."""

    documents: List[Document] = Field(default_factory=list)
    bm25: Any = None
    k: int = 5

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
        **kwargs: Any
    ) -> List[Document]:
        if not self.bm25 or not self.documents:
            return []
        query_tokens = query.lower().split()
        results: List[Document] = self.bm25.get_top_n(
            query_tokens,
            self.documents,
            n=self.k
        )
        return results


class HybridRetriever(BaseRetriever):
    """Hybrid Retriever combining Dense Vector (FAISS) & Sparse Lexical (BM25) via RRF."""

    vector_retriever: Any
    bm25_retriever: Any
    k: int = 5
    rrf_k: int = 60

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
        **kwargs: Any
    ) -> List[Document]:
        # 1. Vector Search
        vector_results: List[Document] = self.vector_retriever.invoke(query)

        # 2. BM25 Search
        bm25_results: List[Document] = self.bm25_retriever.invoke(query)

        # 3. Reciprocal Rank Fusion (RRF)
        scores: Dict[str, float] = {}
        documents: Dict[str, Document] = {}

        # Accumulate Vector RRF scores
        for rank, doc in enumerate(vector_results):
            doc_id = doc.page_content
            documents[doc_id] = doc
            scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        # Accumulate BM25 RRF scores
        for rank, doc in enumerate(bm25_results):
            doc_id = doc.page_content
            documents[doc_id] = doc
            scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        # Sort by combined RRF score
        ranked_documents = sorted(
            documents.values(),
            key=lambda doc: scores[doc.page_content],
            reverse=True
        )

        return ranked_documents[: self.k]


def build_faiss_vector_store(chunks: List[Document], embedding_model: Any) -> FAISS:
    """Build FAISS vector index from document chunks."""
    return FAISS.from_documents(documents=chunks, embedding=embedding_model)


def build_bm25_retriever(chunks: List[Document], k: int = 5) -> BM25Retriever:
    """Build BM25 index from tokenized chunks."""
    tokenized_chunks = [chunk.page_content.lower().split() for chunk in chunks]
    bm25_index = BM25Okapi(tokenized_chunks)
    return BM25Retriever(documents=chunks, bm25=bm25_index, k=k)


def build_hybrid_retriever(
    vector_retriever: BaseRetriever,
    bm25_retriever: BaseRetriever,
    k: int = 5,
    rrf_k: int = 60
) -> HybridRetriever:
    """Instantiate a Hybrid Retriever with configured Top-K and RRF constant."""
    return HybridRetriever(
        vector_retriever=vector_retriever,
        bm25_retriever=bm25_retriever,
        k=k,
        rrf_k=rrf_k
    )


def retrieve_with_details(
    query: str,
    vector_retriever: BaseRetriever,
    bm25_retriever: BaseRetriever,
    k: int = 5,
    rrf_k: int = 60
) -> Dict[str, Any]:
    """
    Execute retrieval and return full diagnostic inspection data for UI visualizer.
    """
    vector_results: List[Document] = vector_retriever.invoke(query)
    bm25_results: List[Document] = bm25_retriever.invoke(query)

    scores: Dict[str, float] = {}
    documents: Dict[str, Document] = {}
    vector_ranks: Dict[str, int] = {}
    bm25_ranks: Dict[str, int] = {}

    for rank, doc in enumerate(vector_results):
        doc_id = doc.page_content
        documents[doc_id] = doc
        vector_ranks[doc_id] = rank + 1
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank + 1))

    for rank, doc in enumerate(bm25_results):
        doc_id = doc.page_content
        documents[doc_id] = doc
        bm25_ranks[doc_id] = rank + 1
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank + 1))

    ranked_documents = sorted(
        documents.values(),
        key=lambda doc: scores[doc.page_content],
        reverse=True
    )

    top_chunks = ranked_documents[:k]

    chunk_diagnostics = []
    for rank, doc in enumerate(top_chunks):
        doc_id = doc.page_content
        page_num = doc.metadata.get("page", 0)
        display_page = page_num + 1 if isinstance(page_num, int) else page_num
        chunk_diagnostics.append({
            "final_rank": rank + 1,
            "page": display_page,
            "rrf_score": round(scores[doc_id], 5),
            "faiss_rank": vector_ranks.get(doc_id, "None"),
            "bm25_rank": bm25_ranks.get(doc_id, "None"),
            "preview": doc.page_content[:140] + ("..." if len(doc.page_content) > 140 else ""),
            "full_content": doc.page_content,
            "metadata": doc.metadata
        })

    return {
        "query": query,
        "vector_count": len(vector_results),
        "bm25_count": len(bm25_results),
        "total_unique": len(documents),
        "top_k_count": len(top_chunks),
        "top_chunks": top_chunks,
        "diagnostics": chunk_diagnostics,
    }
