"""Groq LLM Generation integration with strict RAG grounding."""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from langchain_core.documents import Document
from groq import Groq

load_dotenv()


def get_groq_client(api_key: Optional[str] = None) -> Groq:
    """Initialize Groq client using environment variable or explicit key."""
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found in environment or .env file.")
    return Groq(api_key=key)


def get_available_models() -> List[str]:
    """Return verified working Groq models suitable for QA."""
    try:
        client = get_groq_client()
        models = [m.id for m in client.models.list().data]
        preferred = ["openai/gpt-oss-20b", "qwen/qwen3.8-27b", "openai/gpt-oss-120b", "qwen/qwen3.6-27b"]
        existing_preferred = [p for p in preferred if p in models]
        other_models = [m for m in models if m not in preferred and not m.startswith("whisper")]
        return existing_preferred + other_models
    except Exception:
        return ["openai/gpt-oss-20b", "qwen/qwen3.8-27b", "openai/gpt-oss-120b"]


def build_rag_context(documents: List[Document]) -> str:
    """Format retrieved document chunks into clean numbered context blocks with 1-indexed pages."""
    context_parts = []
    for i, doc in enumerate(documents):
        page = doc.metadata.get("page", "Unknown")
        display_page = page + 1 if isinstance(page, int) else page
        context_parts.append(f"[Source {i + 1} | Page {display_page}]\n{doc.page_content.strip()}")
    return "\n\n".join(context_parts)


def generate_grounded_answer(
    query: str,
    retrieved_documents: List[Document],
    model: str = "openai/gpt-oss-20b",
    temperature: float = 0.2,
    max_tokens: int = 512,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a strictly grounded response using Groq and the retrieved context.
    
    Returns:
        Dict with "answer", "sources", "context", "model", and "success".
    """
    if not retrieved_documents:
        return {
            "answer": "I could not find the answer in the document.",
            "sources": [],
            "context": "",
            "model": model,
            "success": True
        }

    context = build_rag_context(retrieved_documents)

    system_prompt = """You are a helpful document question-answering assistant.

Your job is to answer questions using ONLY the provided document context.

Rules:
1. Use only the provided document context.
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer cannot be found in the context, say:
   "I could not find the answer in the document."
5. Keep the answer concise and easy to understand.
6. When useful, mention the page number.
7. If the document contains a specific number, date, rule, entitlement, or requirement, preserve it accurately."""

    user_prompt = f"""Document Context:

{context}


Question:

{query}


Answer the question using ONLY the document context."""

    # Build sources list for UI citations
    sources = []
    for i, doc in enumerate(retrieved_documents):
        page = doc.metadata.get("page", "Unknown")
        display_page = page + 1 if isinstance(page, int) else page
        sources.append({
            "source_id": i + 1,
            "page": display_page,
            "content": doc.page_content.strip(),
            "metadata": doc.metadata
        })

    try:
        client = get_groq_client(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        answer = response.choices[0].message.content or "I could not find the answer in the document."

        return {
            "answer": answer.strip(),
            "sources": sources,
            "context": context,
            "model": model,
            "success": True,
            "error": None
        }

    except Exception as e:
        return {
            "answer": f"Something went wrong while generating the answer from Groq: {str(e)}",
            "sources": sources,
            "context": context,
            "model": model,
            "success": False,
            "error": str(e)
        }
