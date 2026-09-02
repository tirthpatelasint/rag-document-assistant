"""Custom CSS design system and styling for the Streamlit RAG Document Assistant."""

import streamlit as st


def inject_custom_css():
    """Inject custom modern dark-mode CSS into Streamlit with zero text overlap and protected icon fonts."""
    custom_css = """
    <style>
    /* -------------------------------------------------------------
       FONT IMPORTS & GLOBAL PALETTE
       ------------------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-main: #0B0F19;
        --bg-card: rgba(17, 24, 39, 0.85);
        --bg-card-hover: rgba(31, 41, 55, 0.95);
        --bg-card-solid: #111827;
        --bg-secondary: #1F2937;
        --border-subtle: rgba(255, 255, 255, 0.1);
        --border-accent: rgba(124, 58, 237, 0.45);
        --accent-primary: #7C3AED;
        --accent-primary-gradient: linear-gradient(135deg, #7C3AED 0%, #6366F1 50%, #3B82F6 100%);
        --accent-cyan: #06B6D4;
        --accent-emerald: #10B981;
        --text-main: #F9FAFB;
        --text-muted: #9CA3AF;
        --text-dim: #6B7280;
        --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* Overall Application Background & Font */
    html, body, .stApp {
        background-color: #0B0F19 !important;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(124, 58, 237, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 85% 25%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 50% 85%, rgba(99, 102, 241, 0.08) 0%, transparent 50%) !important;
        background-attachment: fixed !important;
        font-family: var(--font-sans) !important;
        color: #F9FAFB !important;
    }

    /* -------------------------------------------------------------
       CRITICAL: PROTECT MATERIAL SYMBOLS / ICONS FROM FONT OVERRIDE
       (Prevents ligature words like _arrow_right, upload from showing as text)
       ------------------------------------------------------------- */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"],
    [data-testid="stIconMaterial"] *,
    span[translate="no"],
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] span:first-child {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Streamlit Main View Container */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    .main .block-container {
        background: transparent !important;
        color: #F9FAFB !important;
    }

    /* Top Header Bar */
    header[data-testid="stHeader"] {
        background: rgba(11, 15, 25, 0.8) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
        color: #F9FAFB !important;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Specific Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-sans);
        color: #FFFFFF !important;
        font-weight: 700;
    }
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        font-family: var(--font-sans);
    }

    /* -------------------------------------------------------------
       CUSTOM SCROLLBAR
       ------------------------------------------------------------- */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0F19;
    }
    ::-webkit-scrollbar-thumb {
        background: #1F2937;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #374151;
    }

    /* -------------------------------------------------------------
       SIDEBAR STYLING
       ------------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #0D1322 !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
        background-color: #0D1322 !important;
    }
    [data-testid="stSidebarHeader"] {
        background: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"] button {
        color: #9CA3AF !important;
        background: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover {
        color: #FFFFFF !important;
    }

    /* -------------------------------------------------------------
       BOTTOM CHAT INPUT CONTAINER (NO WHITE BOX OVERLAP)
       ------------------------------------------------------------- */
    div[data-testid="stBottom"],
    div[data-testid="stBottom"] > div,
    div[data-testid="stBottomBlockContainer"],
    .stChatInputContainer,
    [data-testid="stChatInputContainer"],
    [data-testid="stBottom"] footer {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Modern Dark Floating Chat Input Box */
    div[data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 1px solid rgba(124, 58, 237, 0.4) !important;
        background: #111827 !important;
        background-color: #111827 !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(124, 58, 237, 0.15) !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #7C3AED !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), 0 0 20px rgba(124, 58, 237, 0.35) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background: transparent !important;
        background-color: transparent !important;
        font-size: 0.95rem !important;
        caret-color: #A78BFA !important;
        font-family: var(--font-sans) !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
    }
    div[data-testid="stChatInput"] button {
        color: #FFFFFF !important;
        background: #7C3AED !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: #6D28D9 !important;
        transform: scale(1.05);
    }
    div[data-testid="stChatInput"] button svg {
        fill: #FFFFFF !important;
    }

    /* -------------------------------------------------------------
       CHAT MESSAGES & BUBBLE STYLING (HIGH CONTRAST)
       ------------------------------------------------------------- */
    div[data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 0.85rem 1.15rem !important;
        border-radius: 14px !important;
        margin-bottom: 1rem !important;
        border: 1px solid var(--border-subtle) !important;
    }

    /* User Message Bubble */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background: rgba(124, 58, 237, 0.12) !important;
        border-color: rgba(124, 58, 237, 0.35) !important;
    }

    /* Assistant Message Bubble */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]),
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        background: rgba(17, 24, 39, 0.75) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* Bright white text for all message contents */
    div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] p,
    div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] span,
    div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] li,
    div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] div {
        color: #F9FAFB !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }
    div[data-testid="stChatMessage"] strong {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    div[data-testid="stChatMessage"] code {
        color: #A78BFA !important;
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-family: var(--font-mono) !important;
    }

    /* Spinner / Generating Status Indicator */
    div[data-testid="stSpinner"],
    div[data-testid="stSpinner"] * {
        color: #C4B5FD !important;
    }
    div[data-testid="stStatusWidget"] {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
    }
    div[data-testid="stStatusWidget"] * {
        color: #E5E7EB !important;
    }

    /* -------------------------------------------------------------
       EXPANDERS (SOURCES & ARCHITECTURE FLOW)
       ------------------------------------------------------------- */
    div[data-testid="stExpander"] {
        background: rgba(17, 24, 39, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        margin-top: 0.75rem !important;
    }
    div[data-testid="stExpander"] summary {
        color: #E5E7EB !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #FFFFFF !important;
        background: rgba(255, 255, 255, 0.03) !important;
    }

    /* -------------------------------------------------------------
       BUTTONS & INTERACTIVE CHIPS
       ------------------------------------------------------------- */
    /* Primary action buttons */
    div.stButton > button[kind="primary"],
    div.stButton > button:not([kind="secondary"]) {
        background: var(--accent-primary-gradient) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        font-family: var(--font-sans) !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.35) !important;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button:not([kind="secondary"]):hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(124, 58, 237, 0.55) !important;
    }

    /* Secondary / Chip buttons */
    div.stButton > button[kind="secondary"] {
        background: rgba(17, 24, 39, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #F3F4F6 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        text-align: center !important;
        font-weight: 500 !important;
        font-family: var(--font-sans) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: rgba(124, 58, 237, 0.2) !important;
        border-color: rgba(124, 58, 237, 0.5) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3) !important;
    }

    /* -------------------------------------------------------------
       SIDEBAR CONTROLS (SLIDER, SELECTBOX, INPUTS)
       ------------------------------------------------------------- */
    .stSlider label, .stSlider p {
        color: #E5E7EB !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        font-family: var(--font-sans) !important;
    }
    .stSlider [data-baseweb="slider"] {
        margin-top: 0.4rem;
    }
    .stSlider div[role="slider"] {
        background-color: #7C3AED !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 10px rgba(124, 58, 237, 0.6) !important;
    }
    .stSlider div[data-testid="stSliderTickBar"] {
        background: rgba(255, 255, 255, 0.15) !important;
    }

    [data-testid="stSelectbox"] label, [data-testid="stSelectbox"] p {
        color: #E5E7EB !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        font-family: var(--font-sans) !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
    }
    [data-testid="stSelectbox"] svg {
        fill: #9CA3AF !important;
    }

    /* -------------------------------------------------------------
       HERO & LANDING CONTAINERS
       ------------------------------------------------------------- */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid rgba(124, 58, 237, 0.4);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #C4B5FD;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        font-family: var(--font-sans);
    }
    .hero-title {
        font-size: 2.75rem !important;
        font-weight: 800 !important;
        line-height: 1.15 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(135deg, #FFFFFF 20%, #E2E8F0 60%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.85rem !important;
        font-family: var(--font-sans) !important;
    }
    .hero-subtitle {
        font-size: 1.125rem !important;
        color: var(--text-muted) !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
        max-width: 650px;
        margin-bottom: 2rem !important;
        font-family: var(--font-sans) !important;
    }

    /* -------------------------------------------------------------
       GLASSMORPHIC FEATURE CARDS
       ------------------------------------------------------------- */
    .feature-card {
        background: var(--bg-card);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1.4rem 1.25rem;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-shadow: var(--glass-shadow);
    }
    .feature-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-accent);
        background: var(--bg-card-hover);
        box-shadow: 0 12px 36px 0 rgba(124, 58, 237, 0.18);
    }
    .feature-icon-wrapper {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.4rem;
        letter-spacing: -0.01em;
        font-family: var(--font-sans);
    }
    .feature-desc {
        font-size: 0.875rem;
        color: var(--text-muted);
        line-height: 1.5;
        font-family: var(--font-sans);
    }

    /* -------------------------------------------------------------
       DOCUMENT STATUS CARD & CHIPS
       ------------------------------------------------------------- */
    .doc-card {
        background: linear-gradient(180deg, rgba(31, 41, 55, 0.7) 0%, rgba(17, 24, 39, 0.9) 100%);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(10px);
    }
    .doc-card-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #FFFFFF;
        word-break: break-all;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 6px;
        font-family: var(--font-sans);
    }
    .doc-stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        color: #D1D5DB;
        font-weight: 500;
        font-family: var(--font-sans);
    }
    .status-badge-ready {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(16, 185, 129, 0.18);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.6rem;
        font-family: var(--font-sans);
    }

    /* System Info Table */
    .system-info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.45rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.8rem;
    }
    .system-info-label {
        color: #9CA3AF;
        font-family: var(--font-sans);
    }
    .system-info-value {
        color: #E5E7EB;
        font-weight: 600;
        font-family: var(--font-mono);
        font-size: 0.76rem;
    }

    /* -------------------------------------------------------------
       EMPTY STATE HERO CONTAINER
       ------------------------------------------------------------- */
    .empty-state-container {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: rgba(17, 24, 39, 0.5);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 18px;
        margin: 1.5rem 0;
    }
    .empty-state-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.4rem;
        font-family: var(--font-sans);
    }
    .empty-state-desc {
        font-size: 0.95rem;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
        font-family: var(--font-sans);
    }

    /* Sources citation card */
    .source-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.75rem;
    }
    .source-box-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    .source-tag {
        background: rgba(124, 58, 237, 0.25);
        border: 1px solid rgba(124, 58, 237, 0.5);
        color: #DDD6FE;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 2px 7px;
        border-radius: 5px;
        font-family: var(--font-sans);
    }
    .page-tag {
        background: rgba(6, 182, 212, 0.2);
        border: 1px solid rgba(6, 182, 212, 0.4);
        color: #A5F3FC;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 2px 7px;
        border-radius: 5px;
        font-family: var(--font-sans);
    }
    .source-content {
        font-size: 0.84rem;
        color: #E2E8F0;
        line-height: 1.5;
        font-family: var(--font-sans);
    }

    /* Retrieval Flow diagram */
    .flow-step {
        display: inline-flex;
        align-items: center;
        background: rgba(31, 41, 55, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #F3F4F6;
        font-family: var(--font-sans);
    }
    .flow-arrow {
        color: var(--accent-cyan);
        font-weight: 700;
        margin: 0 4px;
    }

    /* File uploader styling */
    div[data-testid="stFileUploader"] section {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 2px dashed rgba(124, 58, 237, 0.4) !important;
        border-radius: 14px !important;
        padding: 1.5rem 1rem !important;
    }
    div[data-testid="stFileUploader"] section:hover {
        border-color: #7C3AED !important;
        background: rgba(17, 24, 39, 0.8) !important;
    }
    div[data-testid="stFileUploader"] button {
        background: rgba(124, 58, 237, 0.25) !important;
        border: 1px solid rgba(124, 58, 237, 0.5) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-family: var(--font-sans) !important;
    }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
