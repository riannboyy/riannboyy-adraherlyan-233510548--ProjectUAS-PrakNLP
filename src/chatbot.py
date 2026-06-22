"""
chatbot.py
Inti sistem Smart Study Assistant.
Menggunakan:
  - LangChain  : prompt templates, chains, memory
  - LangGraph  : alur percakapan berbasis state graph
  - LangSmith  : otomatis ter-trace lewat environment variable
"""

import os
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv

# ── LangChain ──────────────────────────────────────────────────────────────
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# ── LangGraph ──────────────────────────────────────────────────────────────
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

load_dotenv()
print("API KEY:", os.getenv("OPENAI_API_KEY"))
# ──────────────────────────────────────────────────────────────────────────
# 1. LLM (LangChain)
# ──────────────────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# ──────────────────────────────────────────────────────────────────────────
# 2. Prompt Templates (LangChain)
# ──────────────────────────────────────────────────────────────────────────
SYSTEM_BASE = """Kamu adalah Smart Study Assistant, asisten belajar cerdas untuk mahasiswa.
Kamu membantu mahasiswa memahami materi kuliah, membuat rangkuman, dan berlatih soal.
Selalu jawab dalam Bahasa Indonesia yang jelas dan mudah dipahami.
Gunakan contoh konkret jika diperlukan."""

SYSTEM_SUMMARIZE = """Kamu adalah Smart Study Assistant yang ahli merangkum materi kuliah.
Buat rangkuman yang terstruktur dengan poin-poin utama, sub-poin, dan kesimpulan.
Gunakan format markdown yang rapi."""

SYSTEM_QUIZ = """Kamu adalah Smart Study Assistant yang membuat soal latihan.
Berikan soal pilihan ganda atau esai yang relevan dengan topik yang diminta.
Sertakan kunci jawaban dan penjelasan singkat."""

SYSTEM_EXPLAIN = """Kamu adalah Smart Study Assistant yang menjelaskan konsep dengan mudah.
Gunakan analogi sederhana, contoh nyata, dan penjelasan bertahap dari dasar hingga lanjutan."""

INTENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tentukan intent dari pesan berikut. Pilih salah satu:
- summarize  : jika user ingin merangkum teks atau materi
- quiz       : jika user ingin dibuatkan soal atau kuis
- explain    : jika user ingin penjelasan konsep
- general    : untuk pertanyaan umum lainnya

Jawab HANYA dengan satu kata intent tersebut, tanpa penjelasan."""),
    ("human", "{message}")
])

def build_chat_prompt(system: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", system),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

# ──────────────────────────────────────────────────────────────────────────
# 3. Graph State (LangGraph)
# ──────────────────────────────────────────────────────────────────────────
class StudyState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    intent: str
    user_input: str
    response: str

# ──────────────────────────────────────────────────────────────────────────
# 4. Node Functions (LangGraph)
# ──────────────────────────────────────────────────────────────────────────

def detect_intent(state: StudyState) -> StudyState:
    """Node: Deteksi intent dari input user menggunakan LangChain chain."""
    intent_chain = INTENT_PROMPT | llm | StrOutputParser()
    detected = intent_chain.invoke({"message": state["user_input"]}).strip().lower()

    valid_intents = {"summarize", "quiz", "explain", "general"}
    intent = detected if detected in valid_intents else "general"
    return {**state, "intent": intent}


def route_intent(state: StudyState) -> str:
    """Edge condition: routing berdasarkan intent."""
    return state["intent"]


def handle_general(state: StudyState) -> StudyState:
    """Node: Jawab pertanyaan umum."""
    prompt = build_chat_prompt(SYSTEM_BASE)
    chain = prompt | llm | StrOutputParser()
    history = list(state["messages"][:-1]) if state["messages"] else []
    response = chain.invoke({"history": history, "input": state["user_input"]})
    return {**state, "response": response}


def handle_summarize(state: StudyState) -> StudyState:
    """Node: Buat rangkuman materi."""
    prompt = build_chat_prompt(SYSTEM_SUMMARIZE)
    chain = prompt | llm | StrOutputParser()
    history = list(state["messages"][:-1]) if state["messages"] else []
    response = chain.invoke({"history": history, "input": state["user_input"]})
    return {**state, "response": response}


def handle_quiz(state: StudyState) -> StudyState:
    """Node: Buat soal kuis."""
    prompt = build_chat_prompt(SYSTEM_QUIZ)
    chain = prompt | llm | StrOutputParser()
    history = list(state["messages"][:-1]) if state["messages"] else []
    response = chain.invoke({"history": history, "input": state["user_input"]})
    return {**state, "response": response}


def handle_explain(state: StudyState) -> StudyState:
    """Node: Jelaskan konsep."""
    prompt = build_chat_prompt(SYSTEM_EXPLAIN)
    chain = prompt | llm | StrOutputParser()
    history = list(state["messages"][:-1]) if state["messages"] else []
    response = chain.invoke({"history": history, "input": state["user_input"]})
    return {**state, "response": response}


def update_memory(state: StudyState) -> StudyState:
    """Node: Simpan pesan ke history (LangChain memory via state)."""
    new_messages = list(state["messages"]) + [AIMessage(content=state["response"])]
    return {**state, "messages": new_messages}

# ──────────────────────────────────────────────────────────────────────────
# 5. Build Graph (LangGraph)
# ──────────────────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    graph = StateGraph(StudyState)

    # Tambahkan nodes
    graph.add_node("detect_intent", detect_intent)
    graph.add_node("handle_general", handle_general)
    graph.add_node("handle_summarize", handle_summarize)
    graph.add_node("handle_quiz", handle_quiz)
    graph.add_node("handle_explain", handle_explain)
    graph.add_node("update_memory", update_memory)

    # Entry point
    graph.set_entry_point("detect_intent")

    # Conditional routing dari detect_intent
    graph.add_conditional_edges(
        "detect_intent",
        route_intent,
        {
            "general":   "handle_general",
            "summarize": "handle_summarize",
            "quiz":      "handle_quiz",
            "explain":   "handle_explain",
        }
    )

    # Setiap handler → update_memory → END
    for node in ["handle_general", "handle_summarize", "handle_quiz", "handle_explain"]:
        graph.add_edge(node, "update_memory")

    graph.add_edge("update_memory", END)

    return graph.compile()

# ──────────────────────────────────────────────────────────────────────────
# 6. StudyAssistant Wrapper
# ──────────────────────────────────────────────────────────────────────────

class StudyAssistant:
    """
    Wrapper class untuk Smart Study Assistant.
    Menyimpan history percakapan dan menjalankan LangGraph.
    LangSmith otomatis meng-trace semua eksekusi jika env var diset.
    """
    def __init__(self):
        self.graph = build_graph()
        self.history: list[BaseMessage] = [
            SystemMessage(content=SYSTEM_BASE)
        ]

    def invoke(self, user_input: str) -> str:
        # Tambahkan pesan user ke history
        self.history.append(HumanMessage(content=user_input))

        # Jalankan graph
        result = self.graph.invoke({
            "messages": self.history,
            "intent": "",
            "user_input": user_input,
            "response": ""
        })

        # Update history dengan balasan AI
        response = result["response"]
        self.history.append(AIMessage(content=response))

        return response


def create_study_assistant() -> StudyAssistant:
    """Factory function untuk membuat instance StudyAssistant."""
    return StudyAssistant()
