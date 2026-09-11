# RemitGuard

> **A Multi-Agent AI Assistant for Safer International Remittances**

RemitGuard is a multi-agent AI assistant designed to help people sending or receiving international remittances — especially migrant-worker families sending money to Bangladesh.

The system helps users:

- Check current exchange rates
- Identify potential scam patterns
- Understand the risks of informal channels such as Hundi/Hawala
- Find safer and regulated transfer channels
- Verify suspicious remittance offers using screenshot-based OCR

RemitGuard combines **LLMs, multi-agent orchestration, web search, Retrieval-Augmented Generation (RAG), vector databases, OCR, and LangSmith tracing** into a single workflow.

---

# Submission Links

| Item | Link |
|---|---|
| **GitHub Repository** | https://github.com/TheKhanSaheb/remit_guard |
| **Demo YouTube Video** | https://youtu.be/JWRYyE_QVxY?si=-kkwgnhHsNgrOASd|
| **Main Application Trace — Scam + RAG + Search** | https://smith.langchain.com/public/189112aa-0573-41f6-93bd-490adc581fd5/r/01a09107-5639-7952-b2a6-221fcc368531?start_time=2026-09-11T15%3A12%3A52.281925Z |
| **Rate Comparator Agent — Rate + Search** | https://smith.langchain.com/public/1570c209-6143-4817-b473-943125d60b56/r/01a0910a-ab6e-70f0-8dba-82ee889a2a03?start_time=2026-09-11T15%3A16%3A30.702233Z |
| **Channel Advisor — RAG + Search** | https://smith.langchain.com/public/f56befb9-63b7-45c0-b7c1-ae16ae3b02e5/r/01a0910d-327b-72e0-a588-336a14efaea5?start_time=2026-09-11T15%3A19%3A16.347955Z |

### LangSmith Trace Evidence

The public LangSmith traces demonstrate the execution of the RemitGuard system, including:

- Agent execution
- LLM invocation
- Internet/web search
- RAG retrieval
- Vector database usage
- Scam risk analysis
- Exchange-rate lookup
- Safe-channel recommendations
- End-to-end workflow execution

---

# 1. About the Project

International remittances are an important source of income for millions of families. However, people sending or receiving money can face several risks, including:

- Unfair exchange rates
- Fraudulent remittance offers
- Fake agents or service providers
- Informal transfer channels
- Hundi/Hawala-related risks
- Lack of access to clear and trustworthy information

In many cases, users need to make decisions quickly but may not know whether an exchange rate, transfer offer, or payment channel is trustworthy.

**RemitGuard addresses this problem by providing an AI-powered assistant that can analyze the user's request using multiple specialized agents and external sources.**

The system combines:

- Live web search for current information
- Regulatory and financial documents through RAG
- LLM-based reasoning
- Scam-pattern analysis
- OCR for suspicious screenshots
- LangGraph-based agent orchestration

Rather than functioning as a general-purpose chatbot, RemitGuard is specifically designed around **remittance safety and verification**.

---

# 2. Target Users

RemitGuard is primarily designed for two groups.

## Remittance Senders

Migrant workers or other users sending money from abroad can use RemitGuard to:

- Check a quoted exchange rate
- Verify information about a transfer service
- Identify suspicious offers
- Understand potential risks before sending money

## Remittance Receivers

Family members or recipients in Bangladesh can use the system to:

- Check unfamiliar transfer methods
- Understand the risks of Hundi/Hawala
- Evaluate suspicious messages or offers
- Learn about safer and regulated alternatives

The system is designed for users without advanced financial knowledge. Therefore, responses are intended to be **simple, practical, and easy to understand**.

---

# 3. Purpose of the Project

The main purpose of RemitGuard is to provide users with a quick and accessible way to make safer remittance decisions.

The system focuses on three main tasks:

1. **Exchange Rate Verification**  
   Check whether a quoted exchange rate is reasonable using current web information.

2. **Scam and Risk Detection**  
   Analyze whether a transfer offer, channel, or message contains potential warning signs.

3. **Safe Channel Recommendation**  
   Recommend regulated and safer remittance channels based on available information.

The overall goal is to help users identify potential risks **before they send or receive money**.

---

# 4. Real-World Impact

Remittance income plays an important role in Bangladesh's economy and in the lives of many families.

However, users can be exposed to financial and legal risks when using unreliable or informal channels.

RemitGuard aims to reduce these risks by helping users:

- Verify information before acting
- Recognize suspicious offers
- Understand Hundi/Hawala-related risks
- Access information from regulatory sources
- Choose safer and regulated transfer options

Even a small improvement in users' ability to verify a rate or transfer channel can help reduce avoidable financial losses.

---

# 5. Why This Needs AI

A traditional FAQ or static information page would not be sufficient for this problem because remittance-related questions can require different types of information and reasoning.

## 5.1 Live Information

Exchange rates change frequently.

A hardcoded exchange rate may quickly become outdated, so RemitGuard uses **web search grounding** to retrieve current information.

## 5.2 Complex Regulatory Information

Financial regulations and AML/CFT reports can be lengthy and difficult for ordinary users to understand.

RemitGuard uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from regulatory and financial documents.

## 5.3 Ambiguous Scam Situations

A question such as:

> "Someone offered me a better exchange rate if I send money through this person. Is it safe?"

cannot always be answered using a simple lookup table.

The system needs to compare the user's situation with known risk patterns and provide a reasoned assessment.

## 5.4 Specialized Agents

Different questions require different tools.

For example:

- Exchange-rate questions → Web Search
- Scam questions → RAG + Search
- Channel questions → RAG + Search
- General questions → General LLM Agent

This is why a **multi-agent architecture** is useful for RemitGuard.

---

# 6. System Architecture

```text
                         User
                          │
                          │
                    Text / Screenshot
                          │
                          ▼
                    Router Agent
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
            Rate        Scam       Channel
            Agent       Agent       Agent
              │           │           │
           Search      RAG +       RAG +
                       Search      Search
              │           │           │
              └───────────┼───────────┘
                          │
                          ▼
                    General Agent
                    (when needed)
                          │
                          ▼
                 Response Aggregator
                          │
                          ▼
                  Final Response
```

## Main Components

**Router Agent**  
Determines which specialized agent should handle the user's request.

**Rate Comparator Agent**  
Uses web search to retrieve current exchange-rate information.

**Scam Detector Agent**  
Uses RAG and web information to identify potential scam or legality risks.

**Channel Advisor Agent**  
Uses regulatory knowledge and web search to recommend safer transfer channels.

**General Agent**  
Handles general remittance-related questions that do not fit the other categories.

**Response Aggregator**  
Provides a consistent final response format for the frontend.

---

# 7. AI Agents

## 7.1 Router Agent

The Router Agent classifies the user's query into one of four categories:

```text
rate
scam
channel
general
```

This allows the system to send each request to the most appropriate specialized agent.

---

## 7.2 Rate Comparator Agent

The Rate Comparator Agent handles exchange-rate questions.

It uses **Tavily web search** to retrieve current information from the internet.

Example query:

```text
What is the current USD to BDT exchange rate today?
```

The retrieved information is then provided to the LLM so that the response is grounded in current web information instead of relying only on model knowledge.

---

## 7.3 Scam Detector Agent

The Scam Detector Agent evaluates potentially suspicious remittance situations.

It uses:

- RAG retrieval
- Regulatory documents
- BFIU information
- FATF reports
- AML/CFT information
- Web search

The agent looks for potential warning signs and explains why a situation may be risky.

The system avoids automatically declaring something a scam without sufficient evidence.

---

## 7.4 Channel Advisor Agent

The Channel Advisor Agent helps users understand safer and regulated remittance options.

It combines:

- RAG knowledge
- Regulatory information
- Web search

The goal is to guide users toward legitimate transfer channels and away from potentially risky informal methods.

---

## 7.5 General Agent

The General Agent acts as a fallback for questions that do not specifically belong to the rate, scam, or channel categories.

---

## 7.6 Response Aggregator

The Response Aggregator converts the selected agent's output into a consistent response structure for the frontend.

This allows the frontend to present responses in a unified way regardless of which agent handled the request.

---

# 8. Screenshot OCR and Scam Analysis

RemitGuard also supports screenshot-based analysis.

A user can upload a screenshot containing a suspicious:

- Message
- Exchange-rate offer
- Remittance advertisement
- Transfer instruction

The backend uses **Tesseract OCR** to extract text from the screenshot.

The extracted text can then be used as input for scam analysis.

```text
Screenshot
    │
    ▼
Tesseract OCR
    │
    ▼
Extracted Text
    │
    ▼
Scam Detector
    │
    ├── RAG Retrieval
    ├── Web Search
    └── LLM Analysis
    │
    ▼
Risk Assessment
```

This allows the system to analyze information that would otherwise require the user to manually type the message.

---

# 9. LLM Resilience

RemitGuard uses a primary/fallback LLM architecture implemented in:

```text
backend/app/llm.py
```

The system first attempts to use **Google Gemini**.

If Gemini is unavailable or encounters an error such as a rate limit, the system falls back to **Groq**.

```text
User Request
     │
     ▼
Google Gemini
     │
     ├── Success ──────► Response
     │
     └── Failure
            │
            ▼
          Groq
            │
            ▼
         Response
```

This improves system resilience by reducing dependence on a single LLM provider.

---

# 10. Project Structure

```text
remitguard/
│
├── .gitignore
├── README.md
│
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   ├── test_rate_agent.py
│   ├── test_router.py
│   ├── test_graph.py
│   │
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── llm.py
│       ├── graph.py
│       │
│       ├── agents/
│       │   ├── router_agent.py
│       │   ├── rate_agent.py
│       │   ├── scam_agent.py
│       │   ├── channel_agent.py
│       │   ├── general_agent.py
│       │   └── aggregator.py
│       │
│       ├── tools/
│       │   ├── search_tool.py
│       │   └── vectorstore_tool.py
│       │
│       └── rag/
│           ├── ingest.py
│           └── data/
│               └── regulatory documents
│
└── frontend/
    ├── package.json
    └── src/
        ├── App.jsx
        ├── App.css
        └── index.css
```

---

# 11. How to Run the Project

This section provides a beginner-friendly setup guide.

## Prerequisites

Install the following:

- **Python 3.10+**
- **Node.js 18+**
- **Git**
- **Tesseract OCR**

### Tesseract OCR

For Windows, install Tesseract using the UB Mannheim build.

The default installation path used by the current backend is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/TheKhanSaheb/remit_guard
cd remitguard
```

---

## Step 2 — Create the Backend Environment

Open a terminal inside the project:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Configure API Keys

Create a `.env` file inside the `backend` directory.

Use `.env.example` as the template.

Required services include:

- Google AI Studio — Gemini
- Groq — fallback LLM
- Tavily — web search
- LangSmith — tracing

Example:

```env
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
```

> **Important:** Never commit `.env` or API keys to GitHub.

---

# 12. Build the RAG Knowledge Base

RemitGuard uses a local vector database containing regulatory and financial documents.

After installing the dependencies, run:

```bash
python -m app.rag.ingest
```

This process:

1. Loads documents from `app/rag/data/`
2. Splits them into smaller chunks
3. Creates local embeddings
4. Stores the embeddings in ChromaDB

The resulting vector database is stored in:

```text
backend/app/rag/chroma_db/
```

---

# 13. Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The backend should start at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 14. Start the Frontend

Open a **new terminal**.

Go to the frontend directory:

```bash
cd remitguard/frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend normally runs at:

```text
http://127.0.0.1:5173
```

Open the URL shown in the terminal.

---

# 15. Example Queries

### Exchange Rate

```text
What is the current USD to BDT exchange rate today?
```

### Scam Detection

```text
Someone offered me a very high USD to BDT rate if I send money through a personal account. Is this safe?
```

### Hundi/Hawala Risk

```text
Is Hundi a safe way to send money to Bangladesh?
```

### Safe Channel

```text
What is the safest way to send money from abroad to Bangladesh?
```

### Screenshot Analysis

Upload a screenshot containing a suspicious remittance message or offer.

---

# 16. RAG Knowledge Base

The Scam Detector and Channel Advisor agents use a Chroma vector database containing relevant regulatory and financial documents.

The knowledge base includes sources related to:

- Bangladesh Bank foreign exchange and remittance regulations
- Bangladesh Money Laundering Prevention Act 2015
- Bangladesh Money Laundering Prevention Rules 2019
- BFIU circulars
- BFIU Annual Report
- APG Bangladesh Mutual Evaluation Report
- FATF reports on Hawala/Hundi and underground banking

The documents are stored in:

```text
backend/app/rag/data/
```

Documents are processed using:

```text
Chunk size:       1200 characters
Chunk overlap:    150 characters
Embedding model:  sentence-transformers/all-MiniLM-L6-v2
Vector database:  ChromaDB
```

The embedding model runs locally, so document ingestion does not require an external embedding API.

---

# 17. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI |
| Agent Orchestration | LangGraph |
| Primary LLM | Google Gemini |
| Fallback LLM | Groq |
| Web Search | Tavily |
| RAG Framework | LangChain |
| Embeddings | HuggingFace Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| OCR | Tesseract + pytesseract |
| Tracing | LangSmith |
| Configuration | Python dotenv / Pydantic Settings |

---

# 18. LangSmith Tracing

RemitGuard uses LangSmith for observing and debugging the AI workflow.

Tracing can provide visibility into:

- Router execution
- Agent execution
- LLM calls
- Web search
- RAG retrieval
- Tool execution
- Workflow execution

Representative public traces are available in the **Submission Links** section at the top of this README.

---

# 19. Requirements Coverage

| Requirement | RemitGuard Implementation |
|---|---|
| Real-world problem | Remittance safety, exchange-rate verification, scam detection, and safe-channel guidance |
| Frontend | React + Vite chat interface |
| Screenshot Upload | Frontend screenshot upload functionality |
| Backend | FastAPI |
| Structured AI Workflow | LangGraph Router → Specialized Agent → Aggregator |
| Multiple Agents | Router, Rate Comparator, Scam Detector, Channel Advisor, General Agent |
| Internet Search | Tavily search tool |
| Search Grounding | Web search results supplied to relevant agents |
| OCR | Tesseract OCR |
| RAG | Regulatory and scam knowledge base |
| Vector Database | ChromaDB |
| Local Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| LLM Resilience | Gemini → Groq fallback |
| LangSmith | Agent, tool, retrieval, and LLM tracing |
| Environment Security | API keys stored in `.env` |
| Documentation | Setup, architecture, workflow, RAG, technology stack, and submission links |

---

# 20. Common Issues

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside the activated virtual environment |
| `ValidationError` on startup | Check that the required API keys exist in `.env` |
| Gemini `429 RESOURCE_EXHAUSTED` | The RAG pipeline uses local HuggingFace embeddings instead of Gemini embeddings |
| Tesseract not found | Install Tesseract and verify the configured executable path |
| CORS error | Make sure the backend is running on port `8000` and the frontend is running on port `5173` |
| Frontend cannot connect to backend | Start the FastAPI backend before using the frontend |

---

# 21. Security

API keys are loaded from environment variables.

The following files should **never** be committed to GitHub:

```text
.env
```

Use:

```text
.env.example
```

to document the required environment variables without exposing secret values.

If an API key has ever been accidentally committed to a public repository, it should be revoked and replaced.

---

# 22. Project Limitations

RemitGuard is designed as an **informational decision-support system**, not as a financial institution, legal advisor, or guaranteed scam-detection service.

Exchange rates and online information can change.

Scam detection is also probabilistic. Therefore, users should verify important financial decisions with trusted banks, regulated financial institutions, or appropriate authorities before transferring money.

---

# 23. Future Improvements

Potential future improvements include:

- More advanced exchange-rate comparison
- Additional remittance service coverage
- Improved OCR preprocessing
- More regulatory documents
- Better structured risk scoring
- More extensive evaluation datasets
- Additional language support
- Improved multi-agent coordination
- Historical rate analysis
- More detailed source attribution

---

# 24. Conclusion

RemitGuard combines **multi-agent AI, real-time web search, RAG, vector databases, OCR, and LLM reasoning** to address a practical financial-safety problem.

Instead of relying on a single general-purpose chatbot, the system uses specialized agents for different remittance-related tasks and grounds their responses using external information and regulatory documents.

The project demonstrates how AI agents can be combined with real-world data sources to provide users with more useful and context-aware assistance for safer remittance decisions.

---
