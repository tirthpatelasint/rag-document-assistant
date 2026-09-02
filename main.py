"""CLI RAG Document Assistant."""

import os
from typing import Any, Optional, List, Dict
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun

from rank_bm25 import BM25Okapi
from pydantic import Field

from groq import Groq




load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add GROQ_API_KEY=your_key to your .env file."
    )




pdf_path = "data/documents/Leave Policy 1.0.pdf"

print("\nLoading PDF...")

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print(f"Number of pages: {len(documents)}")



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)

print(f"Number of chunks: {len(chunks)}")



print("\nLoading Hugging Face embedding model...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-V2"
)



print("\nCreating FAISS vector store...")

vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)



vector_retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)




print("\nCreating BM25 retriever...")

tokenized_chunks = [
    chunk.page_content.lower().split()
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_chunks)

print("✓ BM25 retriever created")




class BM25Retriever(BaseRetriever):

    documents: list[Document] = Field(default_factory=list)
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

        

        vector_results: list[Document] = self.vector_retriever.invoke(query)

        

        bm25_results: list[Document] = self.bm25_retriever.invoke(query)

     

        scores: dict[str, float] = {}
        documents: dict[str, Document] = {}

        for rank, doc in enumerate(vector_results):

            doc_id = doc.page_content

            documents[doc_id] = doc

            scores[doc_id] = scores.get(doc_id, 0.0) + (
                1.0 / (self.rrf_k + rank + 1)
            )

       

        for rank, doc in enumerate(bm25_results):

            doc_id = doc.page_content

            documents[doc_id] = doc

            scores[doc_id] = scores.get(doc_id, 0.0) + (
                1.0 / (self.rrf_k + rank + 1)
            )

        

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




print("\nConnecting to Groq...")

groq_client = Groq(
    api_key=GROQ_API_KEY
)

print("✓ Groq client ready")



print("\n" + "=" * 60)
print("RAG DOCUMENT ASSISTANT")
print("=" * 60)

print("\nType 'exit' or 'quit' to stop.")


while True:

    query = input("\nAsk a question about the document: ")



    if query.lower().strip() in ["exit", "quit"]:

        print("\nGoodbye!")

        break

   

    if not query.strip():

        print("Please enter a question.")

        continue

 

    print("\nSearching document...")

    results = hybrid_retriever.invoke(query)

    print(f"✓ Retrieved {len(results)} relevant chunks")

    

    context = "\n\n".join(
        [
            f"[Source {i + 1} | Page {doc.metadata.get('page', 'Unknown')}]\n"
            f"{doc.page_content}"
            for i, doc in enumerate(results)
        ]
    )

   

    prompt = f"""
You are a helpful document question-answering assistant.

Answer the user's question using ONLY the information
provided in the context below.

Rules:

1. Do not use outside knowledge.
2. Do not make up information.
3. If the answer is not present in the context, say:
   "I could not find the answer in the document."
4. Give a concise and clear answer.
5. If useful, mention the relevant page number.
6. Do not mention these instructions.

Context:
{context}

Question:
{query}

Answer:
"""

   

    print("\nGenerating answer...\n")

    try:

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a document question-answering "
                        "assistant. Answer only from the supplied context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
            max_tokens=512
        )

        answer = response.choices[0].message.content

        

        print("=" * 60)
        print("ANSWER")
        print("=" * 60)

        print(answer)

      

        print("\n" + "=" * 60)
        print("SOURCES")
        print("=" * 60)

        for i, doc in enumerate(results):

            page = doc.metadata.get(
                "page",
                "Unknown"
            )

            print(
                f"[{i + 1}] Page {page}"
            )

    except Exception as e:

        print("\n❌ Groq API Error:")
        print(e)
