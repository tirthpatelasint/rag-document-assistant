"""RAG Pipeline standalone script."""

import os
from typing import Any, Optional, List, Dict
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from rank_bm25 import BM25Okapi

from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun

from pydantic import Field

# IMPORTANT:
# Use the Groq Python SDK, NOT OpenAI/xAI
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not HF_TOKEN:
    raise ValueError(
        "HUGGINGFACE_API_TOKEN not found in .env file"
    )

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )


# ============================================================
# 1. LOAD PDF
# ============================================================

print("\nLoading PDF...")

pdf_path = "data/documents/python123.pdf"

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print("Number of pages:", len(documents))


# ============================================================
# 2. SPLIT DOCUMENTS INTO CHUNKS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)

print("Number of chunks:", len(chunks))


# ============================================================
# 3. HUGGING FACE EMBEDDINGS
# ============================================================

print("\nLoading Hugging Face embedding model...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-V2"
)

print("✓ Embedding model loaded")


# ============================================================
# 4. FAISS VECTOR STORE
# ============================================================

print("\nCreating FAISS vector store...")

vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

print("✓ FAISS vector store created")


# ============================================================
# 5. VECTOR RETRIEVER
# ============================================================

vector_retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 5
    }
)


# ============================================================
# 6. BM25 RETRIEVER
# ============================================================

print("\nCreating BM25 retriever...")

tokenized_chunks = [
    chunk.page_content.lower().split()
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_chunks)

print("✓ BM25 retriever created")


class BM25Retriever(BaseRetriever):

    documents: list[Document] = Field(
        default_factory=list
    )

    bm25: Any = None

    k: int = 5

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
        **kwargs: Any
    ) -> list[Document]:

        query_tokens = query.lower().split()

        results: list[Document] = self.bm25.get_top_n(
            query_tokens,
            self.documents,
            n=self.k
        )

        return results


bm25_retriever = BM25Retriever(
    documents=chunks,
    bm25=bm25,
    k=5
)


# ============================================================
# 7. HYBRID RETRIEVER
# ============================================================

class HybridRetriever(BaseRetriever):

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
    ) -> list[Document]:

        # ----------------------------------------------------
        # Vector search
        # ----------------------------------------------------

        vector_results: list[Document] = self.vector_retriever.invoke(
            query
        )

        # ----------------------------------------------------
        # BM25 search
        # ----------------------------------------------------

        bm25_results: list[Document] = self.bm25_retriever.invoke(
            query
        )

        # ----------------------------------------------------
        # Reciprocal Rank Fusion
        # ----------------------------------------------------

        scores: dict[str, float] = {}

        documents: dict[str, Document] = {}

        # ----------------------------------------------------
        # Vector results
        # ----------------------------------------------------

        for rank, doc in enumerate(vector_results):

            doc_id = doc.page_content

            documents[doc_id] = doc

            scores[doc_id] = (
                scores.get(doc_id, 0.0)
                + 1.0 / (self.rrf_k + rank + 1)
            )

        # ----------------------------------------------------
        # BM25 results
        # ----------------------------------------------------

        for rank, doc in enumerate(bm25_results):

            doc_id = doc.page_content

            documents[doc_id] = doc

            scores[doc_id] = (
                scores.get(doc_id, 0.0)
                + 1.0 / (self.rrf_k + rank + 1)
            )

        # ----------------------------------------------------
        # Sort by combined score
        # ----------------------------------------------------

        ranked_documents = sorted(
            documents.values(),
            key=lambda doc: scores[doc.page_content],
            reverse=True
        )

        return ranked_documents[:self.k]


hybrid_retriever = HybridRetriever(
    vector_retriever=vector_retriever,
    bm25_retriever=bm25_retriever,
    k=5
)


# ============================================================
# 8. CONNECT TO GROQ
# ============================================================

print("\nConnecting to Groq...")

groq_client = Groq(
    api_key=GROQ_API_KEY
)

print("✓ Groq client ready")


# ============================================================
# 9. RAG DOCUMENT ASSISTANT
# ============================================================

print("\n" + "=" * 60)
print("RAG DOCUMENT ASSISTANT")
print("=" * 60)

print("\nType 'exit' or 'quit' to stop.")


while True:

    # --------------------------------------------------------
    # Get question
    # --------------------------------------------------------

    query = input(
        "\nAsk a question about the document: "
    ).strip()

    if query.lower() in ["exit", "quit"]:

        print("\nGoodbye!")

        break

    if not query:

        print("Please enter a question.")

        continue


    # ========================================================
    # 10. RETRIEVE DOCUMENTS
    # ========================================================

    print("\nSearching document...")

    results = hybrid_retriever.invoke(
        query
    )

    print(
        f"✓ Retrieved {len(results)} relevant chunks"
    )


    # ========================================================
    # 11. BUILD CONTEXT
    # ========================================================

    context_parts = []

    for i, doc in enumerate(results):

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        # PDF pages are zero-indexed in LangChain.
        # Add 1 so users see normal page numbers.
        if isinstance(page, int):

            display_page = page + 1

        else:

            display_page = page

        context_parts.append(
            f"[Source {i + 1} | Page {display_page}]\n"
            f"{doc.page_content}"
        )


    context = "\n\n".join(
        context_parts
    )


    # ========================================================
    # 12. SYSTEM PROMPT
    # ========================================================

    system_prompt = """
You are a helpful document question-answering assistant.

Your job is to answer questions using ONLY the provided
document context.

Rules:

1. Use only the provided document context.
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer cannot be found in the context, say:
   "I could not find the answer in the document."
5. Keep the answer concise and easy to understand.
6. When useful, mention the page number.
7. If the document contains a specific number, date,
   rule, entitlement, or requirement, preserve it accurately.
"""


    # ========================================================
    # 13. USER PROMPT
    # ========================================================

    user_prompt = f"""
Document Context:

{context}


Question:

{query}


Answer the question using ONLY the document context.
"""


    # ========================================================
    # 14. CALL GROQ
    # ========================================================

    print("\nGenerating answer...\n")

    try:

        response = groq_client.chat.completions.create(

            # Current Groq production model
            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.2,

            max_tokens=512
        )


        answer = response.choices[0].message.content


        # ====================================================
        # 15. DISPLAY ANSWER
        # ====================================================

        print("=" * 60)
        print("ANSWER")
        print("=" * 60)

        print(answer)


        # ====================================================
        # 16. SHOW SOURCES
        # ====================================================

        print("\n" + "=" * 60)
        print("SOURCES")
        print("=" * 60)

        for i, doc in enumerate(results):

            page = doc.metadata.get(
                "page",
                "Unknown"
            )

            if isinstance(page, int):

                display_page = page + 1

            else:

                display_page = page

            print(
                f"[{i + 1}] Page {display_page}"
            )


    except Exception as e:

        print("\n❌ Groq API Error:")
        print(e)
