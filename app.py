"""Streamlit RAG Document Assistant Application."""

import os
import streamlit as st



from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Community Cloud secrets fallback
if not os.getenv("GROQ_API_KEY"):
    try:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

# Import backend RAG modules
from rag.loader import load_and_split_pdf, get_file_metadata
from rag.embeddings import get_embedding_model
from rag.retriever import (
    build_faiss_vector_store,
    build_bm25_retriever,
    build_hybrid_retriever,
    retrieve_with_details,
)
from rag.generator import (
    generate_grounded_answer,
    get_available_models,
)

# Import UI components and styling
from ui.styles import inject_custom_css
from ui.components import (
    render_header,
    render_hero_landing,
    render_feature_cards,
    render_document_uploader,
    render_sidebar_info,
    render_chat_message,
    render_chat_empty_state,
    get_chat_download_data,
)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS theme
inject_custom_css()


# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
def init_session_state():
    """Initialize persistent Streamlit session state."""
    defaults = {
        "messages": [],
        "processed_doc": None,
        "doc_metadata": {},
        "chunks": [],
        "vector_store": None,
        "vector_retriever": None,
        "bm25_retriever": None,
        "hybrid_retriever": None,
        "top_k": 5,
        "selected_model": "openai/gpt-oss-20b",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


# -----------------------------------------------------------------------------
# RESET HANDLER
# -----------------------------------------------------------------------------
def reset_document_session():
    """Clear active document and chat history to allow uploading another file."""
    st.session_state.processed_doc = None
    st.session_state.doc_metadata = {}
    st.session_state.chunks = []
    st.session_state.vector_store = None
    st.session_state.vector_retriever = None
    st.session_state.bm25_retriever = None
    st.session_state.hybrid_retriever = None
    st.session_state.messages = []


# -----------------------------------------------------------------------------
# DOCUMENT PROCESSING PIPELINE (REAL-TIME PROGRESS)
# -----------------------------------------------------------------------------
def process_uploaded_document(file_source):
    """Execute complete RAG pipeline indexing with real-time status steps."""
    with st.status("Processing document...", expanded=True) as status:
        try:
            # 1. Load & Split PDF
            status.write("📄 Loading and extracting text from PDF...")
            raw_docs, chunks, metadata = load_and_split_pdf(file_source)
            st.session_state.chunks = chunks
            st.session_state.doc_metadata = metadata

            # 2. Embedding Model
            status.write(f"🧠 Loading Hugging Face embeddings (`sentence-transformers/all-MiniLM-L6-V2`)...")
            embedding_model = get_embedding_model()

            # 3. FAISS Vector Store
            status.write(f"⚡ Indexing {len(chunks)} chunks into FAISS vector database...")
            vector_store = build_faiss_vector_store(chunks, embedding_model)
            vector_retriever = vector_store.as_retriever(
                search_kwargs={"k": st.session_state.top_k}
            )
            st.session_state.vector_store = vector_store
            st.session_state.vector_retriever = vector_retriever

            # 4. BM25 Index
            status.write("🔍 Tokenizing text and compiling BM25 Okapi lexical index...")
            bm25_retriever = build_bm25_retriever(chunks, k=st.session_state.top_k)
            st.session_state.bm25_retriever = bm25_retriever

            # 5. Hybrid RRF Retriever
            status.write("🎯 Initializing Reciprocal Rank Fusion (RRF) Hybrid Retriever...")
            hybrid_retriever = build_hybrid_retriever(
                vector_retriever=vector_retriever,
                bm25_retriever=bm25_retriever,
                k=st.session_state.top_k,
                rrf_k=60,
            )
            st.session_state.hybrid_retriever = hybrid_retriever

            # Mark processed
            st.session_state.processed_doc = metadata.get("filename", "Uploaded_Document.pdf")
            status.update(label="✓ Document processed successfully & ready!", state="complete", expanded=False)
            st.rerun()

        except Exception as e:
            status.update(label=f"❌ Error processing document: {str(e)}", state="error", expanded=True)
            st.error(f"Failed to process document: {str(e)}")


# -----------------------------------------------------------------------------
# API KEY VALIDATION BANNER
# -----------------------------------------------------------------------------
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.warning(
        "⚠️ **GROQ_API_KEY is not configured.** Please add your `GROQ_API_KEY` to the `.env` file to enable AI answers.",
        icon="⚠️",
    )


# -----------------------------------------------------------------------------
# MAIN APP ROUTING
# -----------------------------------------------------------------------------
# Fetch available models safely
available_models = get_available_models()
if st.session_state.selected_model not in available_models and available_models:
    st.session_state.selected_model = available_models[0]


# Case 1: NO DOCUMENT UPLOADED YET -> LANDING PAGE
if st.session_state.processed_doc is None:
    render_header()
    render_hero_landing()
    render_feature_cards()

    # Upload Container
    upload_col1, upload_col2, upload_col3 = st.columns([1, 6, 1])
    with upload_col2:
        uploaded_file = render_document_uploader()
        if uploaded_file is not None:
            process_uploaded_document(uploaded_file)


# Case 2: ACTIVE DOCUMENT -> MAIN CHAT WORKSPACE
else:
    # 1. Render Sidebar Controls
    new_top_k, new_model = render_sidebar_info(
        metadata=st.session_state.doc_metadata,
        available_models=available_models,
        current_model=st.session_state.selected_model,
        top_k=st.session_state.top_k,
        on_reset=reset_document_session,
    )

    # Apply changes to top_k or model
    if new_top_k != st.session_state.top_k or new_model != st.session_state.selected_model:
        st.session_state.top_k = new_top_k
        st.session_state.selected_model = new_model
        if st.session_state.vector_store and st.session_state.chunks:
            st.session_state.vector_retriever = st.session_state.vector_store.as_retriever(
                search_kwargs={"k": new_top_k}
            )
            st.session_state.bm25_retriever.k = new_top_k
            st.session_state.hybrid_retriever = build_hybrid_retriever(
                vector_retriever=st.session_state.vector_retriever,
                bm25_retriever=st.session_state.bm25_retriever,
                k=new_top_k,
                rrf_k=60,
            )

    # 2. Main Chat Header
    header_col1, header_col2 = st.columns([5, 5])
    with header_col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; padding: 0.5rem 0 0.5rem 0;">
                <span style="font-size: 1.4rem;">📄</span>
                <div>
                    <h3 style="font-size: 1.2rem; font-weight: 800; margin: 0; color: #FFFFFF;">
                        {st.session_state.doc_metadata.get('filename', 'Document')}
                    </h3>
                    <p style="font-size: 0.78rem; color: #9CA3AF; margin: 0;">
                        {st.session_state.doc_metadata.get('total_pages', 0)} pages • {st.session_state.doc_metadata.get('chunk_count', 0)} chunks • Hybrid RRF (Top-{st.session_state.top_k})
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_col2:
        btn_cols = st.columns([1.2, 1, 1, 1] if st.session_state.messages else [1.2, 2.8])
        with btn_cols[0]:
            if st.button("🚪 Exit Chat", use_container_width=True, type="secondary", help="Exit chat session & return to upload"):
                reset_document_session()
                st.rerun()

        if st.session_state.messages:
            with btn_cols[1]:
                if st.button("🗑️ Clear", use_container_width=True, type="secondary", help="Clear conversation history"):
                    st.session_state.messages = []
                    st.rerun()

            md_export, txt_export = get_chat_download_data(
                st.session_state.messages,
                st.session_state.doc_metadata.get("filename", "document"),
            )
            with btn_cols[2]:
                st.download_button(
                    label="💾 .MD",
                    data=md_export,
                    file_name=f"chat_{st.session_state.doc_metadata.get('filename', 'doc')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            with btn_cols[3]:
                st.download_button(
                    label="📄 .TXT",
                    data=txt_export,
                    file_name=f"chat_{st.session_state.doc_metadata.get('filename', 'doc')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin-bottom: 1.5rem;'>", unsafe_allow_html=True)

    # 3. Render Message History
    for msg in st.session_state.messages:
        render_chat_message(
            role=msg["role"],
            content=msg["content"],
            sources=msg.get("sources"),
            diagnostics=msg.get("diagnostics"),
        )

    # 4. Clean Empty State when no messages
    if not st.session_state.messages:
        render_chat_empty_state(st.session_state.doc_metadata)

    # 5. Handle Chat Input
    user_input = st.chat_input("Ask a question about your document...")

    if user_input:
        # Add user question to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_chat_message(role="user", content=user_input)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Searching document & generating grounded answer..."):
                try:
                    # Retrieve chunks with full diagnostics
                    details = retrieve_with_details(
                        query=user_input,
                        vector_retriever=st.session_state.vector_retriever,
                        bm25_retriever=st.session_state.bm25_retriever,
                        k=st.session_state.top_k,
                        rrf_k=60,
                    )

                    # Call Groq LLM
                    gen_res = generate_grounded_answer(
                        query=user_input,
                        retrieved_documents=details["top_chunks"],
                        model=st.session_state.selected_model,
                        temperature=0.2,
                        max_tokens=512,
                    )

                    answer = gen_res["answer"]
                    sources = gen_res["sources"]
                    diagnostics = details["diagnostics"]

                    # Display Answer
                    st.markdown(answer)

                    # Display Collapsible Sources
                    if sources:
                        from ui.components import render_sources_card, render_retrieval_visualizer
                        render_sources_card(sources)
                        render_retrieval_visualizer(diagnostics)

                    # Save to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "diagnostics": diagnostics,
                    })

                except Exception as e:
                    error_msg = f"Something went wrong while generating the answer: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "sources": [],
                        "diagnostics": [],
                    })

        st.rerun()
