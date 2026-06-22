"""
Smart Study Assistant - UAS NLP
Menggunakan LangChain, LangGraph, dan LangSmith
"""

import os
from dotenv import load_dotenv
import streamlit as st
from chatbot import create_study_assistant

load_dotenv()

st.set_page_config(
    page_title="Study AI",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0e1a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1rem 5rem 1rem !important; max-width: 680px !important; }

/* ══ SIDEBAR ══ */
[data-testid="stSidebar"] {
    background: #0d1221 !important;
    border-right: 1px solid #1a2540 !important;
}
[data-testid="stSidebar"] > div { padding: 1rem 0.85rem !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] span { color: #8898b0 !important; }

.sb-brand {
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 1rem;
    border-bottom: 1px solid #1a2540;
    margin-bottom: 1rem;
}
.sb-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #5b21b6, #1d4ed8);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.sb-name { font-size: 0.82rem !important; font-weight: 700 !important; color: #e2e8f0 !important; line-height: 1.2; }
.sb-tag  { font-size: 0.62rem !important; color: #3d5275 !important; }

.sb-sec { font-size: 0.6rem !important; font-weight: 700 !important; color: #3d5275 !important;
    text-transform: uppercase; letter-spacing: 1.2px; margin: 1rem 0 0.5rem 0 !important; }

.feat {
    display: flex; align-items: flex-start; gap: 9px;
    background: #111827; border: 1px solid #1a2540;
    border-radius: 9px; padding: 0.55rem 0.7rem; margin-bottom: 0.3rem;
}
.feat-dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 4px; flex-shrink: 0; }
.feat-n { font-size: 0.78rem !important; font-weight: 600 !important; color: #c8d6e8 !important; margin: 0 !important; }
.feat-d { font-size: 0.65rem !important; color: #3d5275 !important; margin: 0 !important; }

.smith-card {
    background: rgba(91,33,182,0.1); border: 1px solid rgba(91,33,182,0.25);
    border-radius: 9px; padding: 0.6rem 0.7rem; margin-bottom: 0.5rem;
}
.smith-top { display: flex; align-items: center; gap: 7px; margin-bottom: 0.25rem; }
.smith-led {
    width: 7px; height: 7px; background: #22c55e; border-radius: 50%; flex-shrink: 0;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
.smith-title { font-size: 0.75rem !important; font-weight: 600 !important; color: #a78bfa !important; }
.smith-desc  { font-size: 0.65rem !important; color: #3d5275 !important; line-height: 1.4; }

.stat-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #111827; border: 1px solid #1a2540;
    border-radius: 9px; padding: 0.45rem 0.7rem; margin-bottom: 0.4rem;
}
.stat-lbl { font-size: 0.7rem !important; color: #3d5275 !important; }
.stat-val  { font-size: 0.85rem !important; font-weight: 700 !important; color: #818cf8 !important; }

[data-testid="stSidebar"] .stLinkButton a {
    background: rgba(91,33,182,0.1) !important; border: 1px solid rgba(91,33,182,0.25) !important;
    color: #a78bfa !important; border-radius: 8px !important;
    width: 100% !important; text-align: center !important;
    font-size: 0.72rem !important; padding: 0.4rem !important; display: block !important;
}
[data-testid="stSidebar"] .stButton button {
    background: rgba(239,68,68,0.07) !important; border: 1px solid rgba(239,68,68,0.18) !important;
    color: #f87171 !important; border-radius: 8px !important;
    width: 100% !important; font-size: 0.72rem !important; margin-top: 0.3rem !important;
}

/* ══ HEADER ══ */
.hdr { text-align: center; padding: 1rem 0 0.6rem 0; }
.hdr-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.65rem; font-weight: 700; letter-spacing: -0.3px;
    background: linear-gradient(90deg, #818cf8, #38bdf8, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 0.25rem 0;
}
.hdr-sub { font-size: 0.75rem; color: #3d5275; margin-bottom: 0.7rem; }
.badges  { display: flex; justify-content: center; gap: 0.35rem; margin-bottom: 1.2rem; }
.bdg {
    padding: 0.18rem 0.65rem; border-radius: 999px;
    font-size: 0.65rem; font-weight: 600;
}
.bv { background: rgba(129,140,248,0.12); border: 1px solid rgba(129,140,248,0.3); color: #a5b4fc; }
.bb { background: rgba(56,189,248,0.12);  border: 1px solid rgba(56,189,248,0.3);  color: #7dd3fc; }
.bg { background: rgba(52,211,153,0.12);  border: 1px solid rgba(52,211,153,0.3);  color: #6ee7b7; }

/* ══ WELCOME ══ */
.welcome {
    background: #0d1221; border: 1px solid #1a2540;
    border-radius: 14px; padding: 1.2rem 1.4rem; text-align: center; margin-bottom: 1.2rem;
}
.welcome h3 { font-size: 0.95rem; font-weight: 600; color: #c8d6e8; margin: 0 0 0.3rem 0; }
.welcome p  { font-size: 0.78rem; color: #3d5275; margin: 0 0 0.85rem 0; line-height: 1.5; }
.qbtns { display: flex; flex-wrap: wrap; gap: 0.35rem; justify-content: center; }
.qb {
    background: #111827; border: 1px solid #1e3050;
    border-radius: 999px; padding: 0.25rem 0.75rem;
    font-size: 0.68rem; color: #4a6080;
}


[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 0.55rem !important;
}


[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #1e1b4b !important;
    border: 1px solid #3730a3 !important;
    margin-left: 2.5rem !important;
}


[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: #0d1221 !important;
    border: 1px solid #1a2540 !important;
    border-left: 3px solid #5b21b6 !important;
    margin-right: 2.5rem !important;
}


[data-testid="stChatMessage"] p {
    color: #94a3b8 !important;
    font-size: 0.88rem !important;
    line-height: 1.75 !important;
}
[data-testid="stChatMessage"] li {
    color: #94a3b8 !important;
    font-size: 0.88rem !important;
    line-height: 1.75 !important;
}
[data-testid="stChatMessage"] strong { color: #cbd5e1 !important; font-weight: 600 !important; }
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 { color: #e2e8f0 !important; margin-top: 0.6rem !important; }
[data-testid="stChatMessage"] code {
    background: #1e2a40 !important; color: #7dd3fc !important;
    padding: 0.12rem 0.4rem !important; border-radius: 4px !important; font-size: 0.8rem !important;
}
[data-testid="stChatMessage"] pre {
    background: #070c16 !important; border: 1px solid #1a2540 !important;
    border-radius: 8px !important; padding: 0.8rem !important;
}
[data-testid="stChatMessage"] pre code { color: #a5f3fc !important; background: transparent !important; padding: 0 !important; }

/* ══ INPUT ══ */
[data-testid="stChatInput"] {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #5b21b6 !important;
    box-shadow: 0 0 0 3px rgba(91,33,182,0.15) !important;
}
[data-testid="stChatInput"] textarea {
    color: #0f172a !important;
    background: transparent !important;
    font-size: 0.88rem !important;
    caret-color: #818cf8 !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #243452 !important; }
[data-testid="stSpinner"] p { color: #3d5275 !important; font-size: 0.78rem !important; }
hr { border-color: #1a2540 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assistant" not in st.session_state:
    st.session_state.assistant = create_study_assistant()
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-icon">📚 Study AI</div>
        <div>
            <div class="sb-name">Study AI</div>
            <div class="sb-tag">LangChain · LangGraph · LangSmith</div>
        </div>
    </div>
    <div class="sb-sec">Fitur Chatbot</div>
    <div class="feat">
        <div class="feat-dot" style="background:#818cf8"></div>
        <div><div class="feat-n">General</div><div class="feat-d">Tanya seputar materi kuliah</div></div>
    </div>
    <div class="feat">
        <div class="feat-dot" style="background:#38bdf8"></div>
        <div><div class="feat-n">Summarize</div><div class="feat-d">Rangkum teks atau materi panjang</div></div>
    </div>
    <div class="feat">
        <div class="feat-dot" style="background:#f472b6"></div>
        <div><div class="feat-n">Quiz</div><div class="feat-d">Buat soal + kunci jawaban</div></div>
    </div>
    <div class="feat">
        <div class="feat-dot" style="background:#34d399"></div>
        <div><div class="feat-n">Explain</div><div class="feat-d">Penjelasan konsep dari dasar</div></div>
    </div>
    <div class="sb-sec">Monitoring</div>
    <div class="smith-card">
        <div class="smith-top">
            <div class="smith-led"></div>
            <div class="smith-title">LangSmith Aktif</div>
        </div>
        <div class="smith-desc">Setiap percakapan di-trace: latency, token, alur LangGraph.</div>
    </div>
    """, unsafe_allow_html=True)

    langsmith_url = os.getenv("LANGSMITH_PROJECT_URL", "https://smith.langchain.com")
    st.link_button("Buka Dashboard →", langsmith_url)

    st.markdown(f"""
    <div class="sb-sec" style="margin-top:1rem">Statistik</div>
    <div class="stat-row">
        <span class="stat-lbl">Total pesan</span>
        <span class="stat-val">{st.session_state.msg_count}</span>
    </div>
    <div class="stat-row">
        <span class="stat-lbl">Model</span>
        <span class="stat-val" style="font-size:0.65rem;color:#3d5275">llama-3.3-70b</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑 Hapus Riwayat"):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.session_state.assistant = create_study_assistant()
        st.rerun()

# ── Header ──
st.markdown("""
<div class="hdr">
    <div class="hdr-title">📚 Study AI</div>
    <div class="hdr-sub">Asisten Belajar Cerdas Berbasis AI untuk Mahasiswa</div>
    <div class="badges">
        <span class="bdg bv">⛓ LangChain</span>
        <span class="bdg bb">🕸 LangGraph</span>
        <span class="bdg bg">🔭 LangSmith</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Welcome Box ──
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <h3>👋 Selamat Datang!</h3>
        <p>Saya siap membantu kamu belajar lebih efektif.<br>Coba salah satu contoh berikut:</p>
        <div class="qbtns">
            <span class="qb">📝 Rangkum materi fotosintesis</span>
            <span class="qb">❓ Buat soal algoritma sorting</span>
            <span class="qb">🔍 Jelaskan konsep OOP</span>
            <span class="qb">💬 Apa itu machine learning?</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat History ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat Input ──
if prompt := st.chat_input("Ketik pertanyaan atau materimu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.msg_count += 1
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            response = st.session_state.assistant.invoke(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})