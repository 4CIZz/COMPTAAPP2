import streamlit as st
import anthropic
import base64
import os

st.set_page_config(
    page_title="Questions sur PDF",
    page_icon="📄",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] { background: #080b12 !important; }
[data-testid="stAppViewContainer"] > .main { background: #080b12; padding-bottom: 3rem; }
[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

html, body, p, span, div, label {
    font-family: 'Inter', sans-serif;
    color: #cbd5e1;
}

.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; left: 50%;
    transform: translateX(-50%);
    width: 700px; height: 300px;
    background: radial-gradient(ellipse at center,
        rgba(99,102,241,0.12) 0%,
        rgba(139,92,246,0.06) 40%,
        transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 0.8rem;
    display: block;
}
.hero-title {
    font-family: 'Inter', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.1;
    margin: 0 0 0.6rem;
    letter-spacing: -0.03em;
}
.hero-sub { font-size: 0.95rem; color: #475569; margin: 0; }

.pdf-badge {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    background: #0d1221;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 1rem 1.4rem;
    margin: 0 auto 1.5rem;
    max-width: 860px;
}
.pdf-badge-icon {
    font-size: 1.6rem;
    line-height: 1;
}
.pdf-badge-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #e2e8f0;
    font-weight: 500;
}
.pdf-badge-sub {
    font-size: 0.75rem;
    color: #475569;
    margin-top: 0.1rem;
}
.pdf-badge-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #34d399;
    margin-left: auto;
    flex-shrink: 0;
    box-shadow: 0 0 8px rgba(52,211,153,0.5);
}

.msg-user {
    background: #0d1221;
    border: 1px solid #1e2535;
    border-radius: 14px 14px 4px 14px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0 0.6rem 3rem;
    font-size: 0.93rem;
    color: #e2e8f0;
    line-height: 1.6;
}
.msg-ai {
    background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(139,92,246,0.04));
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 14px 14px 14px 4px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 3rem 0.6rem 0;
    font-size: 0.93rem;
    color: #cbd5e1;
    line-height: 1.7;
}
.msg-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.msg-label.user { color: #475569; }
.msg-label.ai   { color: #6366f1; }

[data-testid="stFileUploader"] {
    background: #0d1221 !important;
    border: 2px dashed #1e2535 !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6366f1 !important;
}
[data-testid="stFileUploader"] label {
    color: #64748b !important;
    font-size: 0.9rem !important;
}

[data-testid="stTextInput"] input {
    background: #0d1221 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.83rem !important;
    padding: 0.55rem 0.75rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
[data-testid="stTextInput"] label {
    color: #475569 !important;
    font-size: 0.8rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stChatInput"] textarea {
    background: #0d1221 !important;
    border: 1px solid #2a3550 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 8px !important;
}

[data-testid="stButton"] > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 25px rgba(99,102,241,0.4) !important;
    transform: translateY(-1px) !important;
}

.api-box {
    background: #0d1221;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    margin: 0 auto 1.5rem;
    max-width: 860px;
}
.api-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.6rem;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #334155;
    font-size: 0.9rem;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }

[data-testid="stSpinner"] { color: #818cf8 !important; }
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ──
for k, v in {"messages": [], "pdf_bytes": None, "pdf_name": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── HERO ──
st.markdown("""
<div class="hero">
    <span class="hero-label">Assistant IA</span>
    <h1 class="hero-title">Questions sur PDF</h1>
    <p class="hero-sub">Déposez un document · Posez vos questions</p>
</div>
""", unsafe_allow_html=True)


# ── CLÉ API ──
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass

if not api_key:
    st.markdown('<div class="api-box"><p class="api-title">Clé API Anthropic</p>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Clé API",
        type="password",
        placeholder="sk-ant-...",
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

if not api_key:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🔑</div>
        Entrez votre clé API Anthropic pour commencer.
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── UPLOAD PDF ──
uploaded = st.file_uploader(
    "Glissez votre PDF ici ou cliquez pour choisir",
    type=["pdf"],
    label_visibility="visible",
)

if uploaded:
    if st.session_state.pdf_name != uploaded.name:
        st.session_state.pdf_bytes = uploaded.read()
        st.session_state.pdf_name = uploaded.name
        st.session_state.messages = []


# ── BADGE PDF ──
if st.session_state.pdf_bytes:
    size_kb = len(st.session_state.pdf_bytes) // 1024
    st.markdown(f"""
    <div class="pdf-badge">
        <div class="pdf-badge-icon">📄</div>
        <div>
            <div class="pdf-badge-name">{st.session_state.pdf_name}</div>
            <div class="pdf-badge-sub">{size_kb} Ko · Prêt pour les questions</div>
        </div>
        <div class="pdf-badge-dot"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── HISTORIQUE ──
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="msg-label user">Vous</div>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-ai">
                <div class="msg-label ai">Claude</div>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

    # ── BOUTON EFFACER ──
    if st.session_state.messages:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Effacer la conversation", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SAISIE QUESTION ──
    question = st.chat_input("Posez une question sur ce document…")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        pdf_b64 = base64.standard_b64encode(st.session_state.pdf_bytes).decode("utf-8")

        # Construit l'historique avec le PDF caché dans le 1er message
        messages_api = []
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                if i == 0:
                    content = [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_b64,
                            },
                            "cache_control": {"type": "ephemeral"},
                        },
                        {"type": "text", "text": msg["content"]},
                    ]
                else:
                    content = msg["content"]
                messages_api.append({"role": "user", "content": content})
            else:
                messages_api.append({"role": "assistant", "content": msg["content"]})

        with st.spinner("Claude lit le document…"):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-opus-4-7",
                    max_tokens=2048,
                    system=(
                        "Tu es un assistant qui répond aux questions sur le document PDF fourni. "
                        "Réponds en français, de façon claire et précise. "
                        "Si la réponse ne se trouve pas dans le document, dis-le franchement."
                    ),
                    messages=messages_api,
                )
                answer = response.content[0].text
            except Exception as e:
                answer = f"Erreur : {e}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📂</div>
        Déposez un fichier PDF ci-dessus pour commencer.
    </div>
    """, unsafe_allow_html=True)
