"""Hugging Face Embedding Model Loader with Streamlit caching."""

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# We provide a cached version for Streamlit and a direct fallback
try:
    import streamlit as st
except ImportError:
    st = None


def _load_model(model_name: str = "sentence-transformers/all-MiniLM-L6-V2") -> HuggingFaceEmbeddings:
    """Instantiate the HuggingFaceEmbeddings model."""
    return HuggingFaceEmbeddings(model_name=model_name)


if st is not None:
    @st.cache_resource(show_spinner=False)
    def get_embedding_model(
        model_name: str = "sentence-transformers/all-MiniLM-L6-V2"
    ) -> HuggingFaceEmbeddings:
        """Cached Hugging Face embedding model singleton across app reruns."""
        return _load_model(model_name)
else:
    def get_embedding_model(
        model_name: str = "sentence-transformers/all-MiniLM-L6-V2"
    ) -> HuggingFaceEmbeddings:
        """Direct Hugging Face embedding model loader."""
        return _load_model(model_name)
