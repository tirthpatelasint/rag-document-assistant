"""Document loader and text chunking utilities."""

import os
import tempfile
from typing import List, Tuple, Dict, Any, Union
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable units."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def get_file_metadata(file_source: Union[str, Any], total_pages: int, chunk_count: int) -> Dict[str, Any]:
    """Extract clean metadata dict for the UI."""
    if isinstance(file_source, str):
        filename = os.path.basename(file_source)
        size_bytes = os.path.getsize(file_source) if os.path.exists(file_source) else 0
    else:
        filename = getattr(file_source, "name", "Document.pdf")
        size_bytes = getattr(file_source, "size", 0)

    return {
        "filename": filename,
        "size_bytes": size_bytes,
        "size_formatted": format_file_size(size_bytes),
        "total_pages": total_pages,
        "chunk_count": chunk_count,
        "status": "Ready",
    }


def load_and_split_pdf(
    file_source: Union[str, Any],
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> Tuple[List[Document], List[Document], Dict[str, Any]]:
    """
    Load a PDF document and split it into chunks.
    
    Args:
        file_source: File path (str) or Streamlit UploadedFile object.
        chunk_size: Maximum chunk size in characters (default: 1000).
        chunk_overlap: Overlap between consecutive chunks (default: 150).
        
    Returns:
        Tuple of (raw_documents, chunks, metadata_dict).
    """
    temp_file_path = None
    try:
        if isinstance(file_source, str):
            if not os.path.exists(file_source):
                raise FileNotFoundError(f"PDF file not found at path: {file_source}")
            loader = PyPDFLoader(file_source)
            raw_docs = loader.load()
        else:
            # Streamlit UploadedFile
            suffix = os.path.splitext(getattr(file_source, "name", ".pdf"))[1] or ".pdf"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_source.getvalue())
                temp_file_path = tmp.name
            
            loader = PyPDFLoader(temp_file_path)
            raw_docs = loader.load()

        if not raw_docs:
            raise ValueError("The uploaded PDF appears to be empty or could not be read.")

        # Ensure page numbers in metadata are clean
        for i, doc in enumerate(raw_docs):
            if "page" not in doc.metadata:
                doc.metadata["page"] = i

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(raw_docs)

        metadata = get_file_metadata(
            file_source=file_source,
            total_pages=len(raw_docs),
            chunk_count=len(chunks)
        )

        return raw_docs, chunks, metadata

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass
