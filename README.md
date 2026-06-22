# 📚 Smart Study Assistant

> Asisten belajar cerdas berbasis AI untuk mahasiswa — dibangun dengan **LangChain**, **LangGraph**, dan **LangSmith**.

---



**Smart Study Assistant** adalah chatbot berbasis LLM yang dirancang untuk membantu mahasiswa dalam proses belajar. Chatbot ini mampu:

- 💬 **Menjawab pertanyaan** umum seputar materi kuliah
- 📝 **Merangkum materi** secara terstruktur dengan poin-poin utama
- ❓ **Membuat soal kuis** pilihan ganda dan esai beserta kunci jawaban
- 🔍 **Menjelaskan konsep** secara bertahap dengan analogi dan contoh nyata
- 🧠 **Mengingat konteks** percakapan sebelumnya (conversation memory)

Sistem ini dibangun sebagai proyek UAS Mata Kuliah Natural Language Processing (NLP) yang wajib mengintegrasikan tiga library: **LangChain**, **LangGraph**, dan **LangSmith**.

---

##  Arsitektur Sistem

```
User Input
    │
    ▼
┌─────────────────────────────────────────────┐
│              LangGraph State Graph           │
│                                             │
│  ┌─────────────┐     ┌───────────────────┐  │
│  │detect_intent│────▶│  route_intent()   │  │
│  │ (LangChain) │     │  (conditional     │  │
│  └─────────────┘     │   edge)           │  │
│                      └────────┬──────────┘  │
│              ┌─────────┬──────┴──┬────────┐ │
│              ▼         ▼         ▼        ▼ │
│         general  summarize    quiz    explain│
│              │         │         │        │ │
│              └─────────┴────┬────┴────────┘ │
│                             ▼               │
│                      update_memory          │
│                             │               │
│                            END              │
└─────────────────────────────────────────────┘
    │
    ▼
Response + LangSmith Trace
```

---

##  Teknologi yang Digunakan

| Library | Versi | Kegunaan dalam Proyek |
|---------|-------|----------------------|
| **LangChain** | 0.3.x | Prompt templates, LLM chains, output parser, memory management |
| **LangGraph** | 0.4.x | State graph, node routing, conditional edges, conversation flow |
| **LangSmith** | 0.3.x | Automatic tracing, monitoring latency & token usage, debugging |
| Streamlit | 1.45.x | Web UI chatbot |
| OpenAI GPT-4o-mini | — | Model LLM utama |

---

##  Cara Menjalankan Program

### 1. Clone Repository

```bash
git clone https://github.com/username/smart-study-assistant.git
cd smart-study-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
cp .env.example .env
```

Buka file `.env` dan isi dengan API key kamu:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here

LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=ls__your-langsmith-api-key-here
LANGCHAIN_PROJECT=smart-study-assistant
```

> **Cara mendapatkan API Key:**
> - **GrocAI**: https://console.groq.com
> - **LangSmith**: https://smith.langchain.com → Settings → API Keys

### 4. Jalankan Aplikasi

```bash
cd src
streamlit run app.py
```

Buka browser di: **http://localhost:8501**

---

##  Screenshot

### Tampilan Utama Chatbot
![Main Interface][text](docs/screenshoot/tampilan1)

### Contoh: Merangkum Materi
![Summarize Feature][text](docs/screenshoot/tampilan2)

### Contoh: Membuat Soal Kuis
![Quiz Feature](docs/screenshots/quiz.png)

### LangSmith Dashboard - Trace Monitoring
![LangSmith Trace](docs/screenshots/langsmith-trace.png)

### LangGraph - Alur State Graph
![LangGraph Flow](docs/screenshots/langgraph-flow.png)

---

##  Penjelasan Penggunaan Library

### 🔗 LangChain
LangChain digunakan untuk:
- **`ChatPromptTemplate`** — Membuat prompt yang berbeda-beda sesuai intent (general, summarize, quiz, explain)
- **`MessagesPlaceholder`** — Menyisipkan riwayat percakapan ke dalam prompt
- **`ChatOpenAI`** — Wrapper LLM yang terintegrasi dengan LangSmith
- **`StrOutputParser`** — Parsing output dari LLM menjadi string
- **Chain (`|` operator)** — Menghubungkan prompt → LLM → parser secara deklaratif

```python
# Contoh penggunaan LangChain chain
intent_chain = INTENT_PROMPT | llm | StrOutputParser()
detected = intent_chain.invoke({"message": user_input})
```

###  LangGraph
LangGraph digunakan untuk:
- **`StateGraph`** — Mendefinisikan alur percakapan sebagai directed graph
- **`TypedDict` State** — Menyimpan state: messages, intent, user_input, response
- **`add_messages`** — Reducer untuk mengelola history pesan
- **`add_conditional_edges`** — Routing dinamis berdasarkan hasil deteksi intent
- **Node functions** — Setiap mode (general/summarize/quiz/explain) adalah node tersendiri

```python
# Contoh conditional routing di LangGraph
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
```

###  LangSmith
LangSmith digunakan untuk:
- **Automatic tracing** — Semua eksekusi LangChain/LangGraph otomatis ter-trace
- **Latency monitoring** — Memantau waktu respons setiap node
- **Token usage** — Melacak penggunaan token per request
- **Run visualization** — Visualisasi alur eksekusi di dashboard

```env
# Cukup set environment variable, LangSmith aktif otomatis
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your-key
LANGCHAIN_PROJECT=smart-study-assistant
```

---

##  Struktur Proyek

```
smart-study-assistant/
├── src/
│   ├── app.py          # Streamlit UI
│   └── chatbot.py      # LangChain + LangGraph + LangSmith
├── docs/
│   └── screenshots/    # Screenshot untuk README
├── .env.example        # Template environment variables
├── requirements.txt    # Dependencies
└── README.md
```

---

##  Informasi Mahasiswa

| | |
|---|---|
| **Nama** | [Nama Kamu] |
| **NIM** | [NIM Kamu] |
| **Mata Kuliah** | Natural Language Processing (NLP) |
| **Dosen** | [Nama Dosen] |
| **Tahun** | 2025 |

---

##  Lisensi

Proyek ini dibuat untuk keperluan akademik (UAS NLP).
