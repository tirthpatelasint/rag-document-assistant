"""Reusable UI components for the Streamlit RAG Document Assistant."""

import streamlit as st
from typing import List, Dict, Any, Optional, Callable


def render_header():
    """Render top application header."""
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 0 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);">
                    ⚡
                </div>
                <div>
                    <h2 style="font-size: 1.35rem; font-weight: 800; margin: 0; color: #FFFFFF; letter-spacing: -0.02em;">RAG Document Assistant</h2>
                    <p style="font-size: 0.82rem; color: #9CA3AF; margin: 0;">Intelligent Hybrid Retrieval • FAISS + BM25 • Groq LLM</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 0.75rem; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; padding: 4px 10px; border-radius: 9999px; font-weight: 600;">
                    ● System Active
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_landing():
    """Render hero section for landing page."""
    st.markdown(
        """
        <div style="text-align: center; max-width: 800px; margin: 1.5rem auto 2.5rem auto;">
            <div class="hero-badge">
                ✨ Enterprise-Grade Hybrid RAG
            </div>
            <h1 class="hero-title">
                Chat with your documents using AI.
            </h1>
            <p class="hero-subtitle" style="margin: 0 auto 2rem auto;">
                Upload any PDF document and ask questions with deep confidence. Powered by dense semantic vector search, BM25 keyword matching, Reciprocal Rank Fusion, and lightning-fast Groq inference.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards():
    """Render 4 interactive glassmorphic capability cards."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon-wrapper" style="background: rgba(124, 58, 237, 0.18); color: #C4B5FD;">
                    🧠
                </div>
                <div class="feature-title">Semantic Search</div>
                <div class="feature-desc">
                    Hugging Face embeddings and FAISS vector index to deeply understand conceptual meaning.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon-wrapper" style="background: rgba(6, 182, 212, 0.18); color: #67E8F9;">
                    🔍
                </div>
                <div class="feature-title">Keyword Search</div>
                <div class="feature-desc">
                    BM25 Okapi lexical engine matching exact acronyms, numbers, codes, and specific terms.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon-wrapper" style="background: rgba(245, 158, 11, 0.18); color: #FCD34D;">
                    ⚡
                </div>
                <div class="feature-title">Hybrid Retrieval</div>
                <div class="feature-desc">
                    Reciprocal Rank Fusion (RRF) algorithm combining dense vector and lexical rankings seamlessly.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon-wrapper" style="background: rgba(16, 185, 129, 0.18); color: #6EE7B7;">
                    🎯
                </div>
                <div class="feature-title">Grounded Answers</div>
                <div class="feature-desc">
                    Strict prompt engineering on Groq LLMs guaranteeing zero hallucination and clear citations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_document_uploader(on_upload_callback: Optional[Callable] = None):
    """Render modern drag-and-drop document upload area."""
    st.markdown(
        """
        <div style="margin: 2.5rem 0 1rem 0;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                <span style="font-size: 1.1rem; font-weight: 700; color: #F9FAFB;">📄 Upload Document</span>
                <span style="font-size: 0.78rem; background: rgba(255,255,255,0.06); padding: 2px 8px; border-radius: 4px; color: #9CA3AF;">PDF Supported</span>
            </div>
            <p style="font-size: 0.85rem; color: #9CA3AF; margin-bottom: 1rem;">
                Select a document from your device or drag and drop a PDF below to initiate processing.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        label="Drop your document here (PDF files supported)",
        type=["pdf"],
        label_visibility="collapsed",
        key="pdf_uploader",
    )
    return uploaded_file


def render_sidebar_info(
    metadata: Dict[str, Any],
    available_models: List[str],
    current_model: str,
    top_k: int,
    on_reset: Callable,
    on_settings_change: Optional[Callable] = None,
):
    """Render modern, informative sidebar."""
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1.25rem;">
                <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%); display: flex; align-items: center; justify-content: center; font-size: 1rem;">
                    ⚡
                </div>
                <span style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF;">Document Assistant</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 1. Document Details Card
        if metadata:
            st.markdown(
                f"""
                <div class="doc-card">
                    <div class="doc-card-title">
                        <span>📄</span>
                        <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{metadata.get('filename', 'Document.pdf')}</span>
                    </div>
                    <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px;">
                        <span class="doc-stat-pill">📖 {metadata.get('total_pages', 0)} pages</span>
                        <span class="doc-stat-pill">🧩 {metadata.get('chunk_count', 0)} chunks</span>
                        <span class="doc-stat-pill">💾 {metadata.get('size_formatted', '0 KB')}</span>
                    </div>
                    <div style="margin-top: 8px;">
                        <span class="status-badge-ready">
                            ✓ {metadata.get('status', 'Ready')}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 2. Reset / Exit Document Buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("➕ New Doc", use_container_width=True, type="primary", help="Upload another document"):
                on_reset()
                st.rerun()
        with col_btn2:
            if st.button("🚪 Quit Chat", use_container_width=True, type="secondary", help="Exit chat and return to upload screen"):
                on_reset()
                st.rerun()

        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 1.25rem 0;'>", unsafe_allow_html=True)

        # 3. Retrieval Settings
        st.markdown("<p style='font-size: 0.85rem; font-weight: 700; color: #E5E7EB; margin-bottom: 0.5rem;'>⚙️ Retrieval Settings</p>", unsafe_allow_html=True)
        
        new_top_k = st.slider(
            "Top-K Chunks to Retrieve",
            min_value=1,
            max_value=10,
            value=top_k,
            help="Number of most relevant chunks passed to the LLM context",
            key="top_k_slider",
        )

        # Model Selector
        model_idx = available_models.index(current_model) if current_model in available_models else 0
        new_model = st.selectbox(
            "Groq LLM Model",
            options=available_models,
            index=model_idx,
            key="model_selector",
        )

        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 1.25rem 0;'>", unsafe_allow_html=True)

        # 4. System Specifications
        st.markdown(
            """
            <p style='font-size: 0.85rem; font-weight: 700; color: #E5E7EB; margin-bottom: 0.5rem;'>🛠️ System Architecture</p>
            <div style="background: rgba(17, 24, 39, 0.4); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 0.75rem;">
                <div class="system-info-row">
                    <span class="system-info-label">Embeddings:</span>
                    <span class="system-info-value" title="sentence-transformers/all-MiniLM-L6-V2">all-MiniLM-L6-V2</span>
                </div>
                <div class="system-info-row">
                    <span class="system-info-label">Vector DB:</span>
                    <span class="system-info-value">FAISS CPU</span>
                </div>
                <div class="system-info-row">
                    <span class="system-info-label">Keyword Engine:</span>
                    <span class="system-info-value">BM25 Okapi</span>
                </div>
                <div class="system-info-row">
                    <span class="system-info-label">Fusion Algorithm:</span>
                    <span class="system-info-value">Hybrid RRF (k=60)</span>
                </div>
                <div class="system-info-row" style="border-bottom: none;">
                    <span class="system-info-label">Inference:</span>
                    <span class="system-info-value">Groq Cloud</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="text-align: center; margin-top: 1.5rem; font-size: 0.72rem; color: #6B7280;">
                🔒 Strict Context Grounding • Zero Hallucination
            </div>
            """,
            unsafe_allow_html=True,
        )

        return new_top_k, new_model


def render_sources_card(sources: List[Dict[str, Any]]):
    """Render collapsible source citations with page tags and chunk text."""
    if not sources:
        return

    with st.expander(f"📚 View Sources & Citations ({len(sources)} chunks retrieved)", expanded=False):
        for s in sources:
            source_id = s.get("source_id", 1)
            page = s.get("page", 1)
            content = s.get("content", "")
            
            st.markdown(
                f"""
                <div class="source-box">
                    <div class="source-box-header">
                        <span class="source-tag">📄 Source {source_id}</span>
                        <span class="page-tag">Page {page}</span>
                    </div>
                    <div class="source-content">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_retrieval_visualizer(diagnostics: Optional[List[Dict[str, Any]]] = None):
    """Render visual RAG flow diagram and retrieval rank fusion breakdown."""
    with st.expander("🔍 Retrieval Architecture & Ranking Flow", expanded=False):
        # 1. Flow Diagram
        st.markdown(
            """
            <div style="padding: 0.75rem; background: rgba(15, 23, 42, 0.4); border-radius: 10px; margin-bottom: 1rem; text-align: center;">
                <div style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 6px;">
                    <span class="flow-step">👤 User Query</span>
                    <span class="flow-arrow">➔</span>
                    <span class="flow-step" style="border-color: rgba(124, 58, 237, 0.4);">🧠 FAISS Vector</span>
                    <span style="color: #6B7280; font-size: 0.8rem;">+</span>
                    <span class="flow-step" style="border-color: rgba(6, 182, 212, 0.4);">🔍 BM25 Lexical</span>
                    <span class="flow-arrow">➔</span>
                    <span class="flow-step" style="border-color: rgba(245, 158, 11, 0.4);">⚡ RRF Ranking</span>
                    <span class="flow-arrow">➔</span>
                    <span class="flow-step">📦 Top-K Context</span>
                    <span class="flow-arrow">➔</span>
                    <span class="flow-step" style="border-color: rgba(16, 185, 129, 0.4);">🤖 Groq LLM</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Detailed RRF Table if diagnostics available
        if diagnostics:
            st.markdown(
                """
                <p style="font-size: 0.82rem; font-weight: 600; color: #D1D5DB; margin-bottom: 0.5rem;">
                    Chunk Ranking & Score Matrix:
                </p>
                """,
                unsafe_allow_html=True,
            )
            for diag in diagnostics:
                rank = diag.get("final_rank", 1)
                page = diag.get("page", 1)
                rrf_score = diag.get("rrf_score", 0.0)
                faiss_r = diag.get("faiss_rank", "-")
                bm25_r = diag.get("bm25_rank", "-")
                preview = diag.get("preview", "")
                
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(31, 41, 55, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 6px 12px; margin-bottom: 6px; font-size: 0.78rem;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-weight: 700; color: #A78BFA;">#{rank}</span>
                            <span style="color: #67E8F9; font-weight: 600;">Page {page}</span>
                            <span style="color: #9CA3AF; font-size: 0.75rem;">FAISS: #{faiss_r} | BM25: #{bm25_r}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="color: #FCD34D; font-family: var(--font-mono); font-weight: 600;">Score: {rrf_score}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_chat_empty_state(metadata: Optional[Dict[str, Any]] = None):
    """Render clean document readiness empty state container without pre-set questions."""
    doc_name = metadata.get("filename", "Your document") if metadata else "Your document"
    total_pages = metadata.get("total_pages", "") if metadata else ""
    page_str = f" ({total_pages} pages)" if total_pages else ""

    st.markdown(
        f"""
        <div class="empty-state-container">
            <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">📄✨</div>
            <div class="empty-state-title">{doc_name}{page_str} is ready</div>
            <div class="empty-state-desc">Ask any question in the box below to query your document.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_chat_download_data(messages: List[Dict[str, Any]], filename: str) -> tuple[str, str]:
    """Generate Markdown and TXT formatted string exports of conversation."""
    md_lines = [f"# RAG Assistant Conversation Log\n**Document:** {filename}\n\n---\n"]
    txt_lines = [f"RAG Assistant Conversation Log\nDocument: {filename}\n\n" + "=" * 50 + "\n"]

    for msg in messages:
        role = "User" if msg["role"] == "user" else "AI Assistant"
        content = msg.get("content", "")
        
        md_lines.append(f"### {role}\n{content}\n")
        txt_lines.append(f"{role}:\n{content}\n\n")

        if msg.get("sources"):
            md_lines.append("**Sources:**\n")
            txt_lines.append("Sources:\n")
            for s in msg["sources"]:
                md_lines.append(f"- Source {s.get('source_id', '')} (Page {s.get('page', '')})\n")
                txt_lines.append(f"- Source {s.get('source_id', '')} (Page {s.get('page', '')})\n")
            md_lines.append("\n")
            txt_lines.append("\n")

    return "\n".join(md_lines), "\n".join(txt_lines)


def render_chat_message(role: str, content: str, sources: Optional[List[Dict[str, Any]]] = None, diagnostics: Optional[List[Dict[str, Any]]] = None):
    """Render a styled conversational chat bubble with avatar and citations."""
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
        if sources:
            render_sources_card(sources)
        if diagnostics:
            render_retrieval_visualizer(diagnostics)
