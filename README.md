# RemitGuard

**Know before you send.** RemitGuard is a multi-agent AI assistant that helps people sending or receiving international remittances — especially migrant-worker families sending money to Bangladesh — check exchange rates, spot scam patterns, and choose safe, legal transfer channels before they send money.

## 1. The Problem

Bangladesh receives billions of dollars in remittances every year, much of it from migrant workers abroad. Their families back home frequently face three recurring problems:

- **Unclear exchange rates** — it's hard to know if a quoted rate is fair or if someone is quietly shortchanging them.
- **Scam and informal-channel risk** — offers of a "better rate" through unregulated channels (hundi/hawala) are common, illegal, and carry real financial and legal risk.
- **Confusing channel choice** — banks, mobile financial services, and money transfer operators all have different fees, speeds, and legitimacy, and it's not always obvious which is safest for a given situation.

**Target user:** a remittance sender or receiver (often not financially sophisticated) who wants a quick, trustworthy second opinion before completing a transfer.

**Why AI helps:** the right answer depends on combining live market data (search), authoritative regulatory knowledge (RAG over real Bangladesh Bank/BFIU/FATF documents), and judgment about risk — which is exactly the kind of multi-source reasoning task agents are suited for.

## 2. Architecture

```
User query (text or screenshot)
        │
        ▼
   Router Agent  ──classifies intent──▶ rate | scam | channel | general
        │
   ┌────┴────┬─────────┬──────────┐
   ▼         ▼         ▼          ▼
Rate      Scam      Channel    General
Agent     Agent     Agent      Agent
(search) (RAG)   (RAG+search) (LLM)
   │         │         │          │
   └────┬────┴─────────┴──────────┘
        ▼
   Response Aggregator
        │
        ▼
   Final structured answer
```

- **Router Agent** — classifies the user's query into `rate`, `scam`, `channel`, or `general` using an LLM call.
- **Rate Comparator Agent** — uses Tavily web search (search grounding) to answer live exchange-rate questions.
- **Scam Detector Agent** — retrieves relevant chunks from the RAG knowledge base (Bangladesh AML law, BFIU circulars, FATF hawala/hundi reports) to assess whether a described channel or offer looks fraudulent.
- **Channel Advisor Agent** — combines RAG + web search to recommend regulated, legal transfer channels.
- **General Agent** — a fallback for anything outside the above three categories.
- **Response Aggregator** — formats the selected agent's output into a consistent structured response for the frontend.
- **OCR + Scam Detector integration** (`/analyze-screenshot`) — a user can upload a screenshot of a suspicious message/offer; the backend runs OCR on it and feeds the extracted text into the Scam Detector Agent for analysis, so OCR is part of the actual reasoning workflow rather than a standalone utility.

All LLM calls go through a primary/fallback wrapper (`app/llm.py`): Gemini is tried first, and the system automatically falls back to Groq if Gemini is unavailable or rate-limited, so a single provider hiccup doesn't take down the whole app.

## 3. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite) |
| Backend | FastAPI |
| Agent orchestration | LangGraph |
| Primary LLM | Google Gemini (via `langchain-google-genai`) |
| Fallback LLM | Groq (`openai/gpt-oss-120b`) |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (local, no API rate limits) |
| Vector database | ChromaDB |
| Internet search / grounding | Tavily |
| OCR | Tesseract (via `pytesseract`) |
| Tracing / observability | LangSmith |

## 4. RAG Knowledge Base

The Scam Detector and Channel Advisor agents retrieve from a Chroma vector store built from real regulatory documents, including:

- Bangladesh Bank foreign exchange / remittance circulars
- Bangladesh Money Laundering Prevention Act (2015) & Rules (2019)
- BFIU circulars and Annual Report
- APG Bangladesh Mutual Evaluation Report
- FATF reports on hawala/hundi and underground banking

Documents live in `backend/app/rag/data/` and are chunked (1200 chars, 150 overlap) and embedded locally before being stored in Chroma.

## 5. Project Structure

```
remitguard/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, routes (/chat, /ocr, /analyze-screenshot)
│   │   ├── config.py             # Settings loaded from .env
│   │   ├── llm.py                # Primary/fallback LLM wrapper
│   │   ├── graph.py              # LangGraph orchestration (router → agents → aggregator)
│   │   ├── agents/
│   │   │   ├── router_agent.py
│   │   │   ├── rate_agent.py
│   │   │   ├── scam_agent.py
│   │   │   ├── channel_agent.py
│   │   │   ├── general_agent.py
│   │   │   └── aggregator.py
│   │   ├── tools/
│   │   │   ├── search_tool.py    # Tavily search grounding
│   │   │   └── vectorstore_tool.py # Chroma retrieval
│   │   └── rag/
│   │       ├── ingest.py         # Chunk + embed documents into Chroma
│   │       └── data/             # Source PDFs/TXT
│   └── requirements.txt
├── frontend/
│   └── src/App.jsx
└── README.md
```

## 6. Setup

### Backend

```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

Create `backend/.env` (see `.env.example` below for required keys), then build the RAG index once:

```bash
python -m app.rag.ingest
```

Run the API:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://127.0.0.1:8000`.

## 7. Environment Variables

```
GOOGLE_API_KEY=
GROQ_API_KEY=
TAVILY_API_KEY=

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=remitguard

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=remitguard

APP_ENV=development

# Optional — only needed if Tesseract is not on your system PATH
TESSERACT_CMD=
```

Never commit `.env` — it's already excluded via `.gitignore`.

## 8. LangSmith Tracing

Every agent call, tool call, and LLM invocation is traced to LangSmith under the `remitguard` project once `LANGSMITH_TRACING=true` and a valid `LANGSMITH_API_KEY` are set. Trace links demonstrating router → agent → aggregator execution are included in the project submission.

## 9. Disclaimer

RemitGuard provides informational guidance only. It does not replace advice from a bank or a licensed money transfer operator, and users should always verify details before sending money.
