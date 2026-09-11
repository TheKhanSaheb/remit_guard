**# RemitGuard**

**\*\*Know before you send.\*\***

RemitGuard is a multi-agent AI assistant that helps people sending or receiving international remittances — especially migrant-worker families sending money to Bangladesh — check exchange rates, spot scam patterns, and choose safe, legal transfer channels before they send money.

**---**

**## 1. About the Project**

Every year, millions of migrant workers send money home to their families, and every year a meaningful share of that money is lost to unfair exchange rates, informal "hundi"/hawala channels, or outright scams — simply because the sender or receiver had no quick, trustworthy way to check whether a rate, a message, or a transfer method was legitimate before acting on it.

RemitGuard is not a general-purpose chatbot. It's a purpose-built assistant that takes a user's question (or a screenshot of a suspicious offer) and routes it to one of several specialized AI agents, each backed by real data: live web search for current rates, and a knowledge base built from actual Bangladesh Bank, BFIU, and FATF regulatory documents for scam/legality questions.

**## 2. Target User**

\- A **\*\*remittance sender abroad\*\*** (a migrant worker) who wants to confirm a quoted exchange rate or check whether a transfer offer looks legitimate before sending money.

\- A **\*\*remittance receiver in Bangladesh\*\*** (often a family member) who is offered an unfamiliar transfer method or a "special rate" and wants a second opinion.

\- Neither user is assumed to be financially sophisticated — the app is built to explain things in plain language, not jargon.

**## 3. Purpose of the Project**

To give remittance senders and receivers a fast, independent way to:

1\. Check whether a quoted exchange rate is reasonable.

2\. Assess whether a transfer channel or offer shows signs of being a scam or an illegal channel (hundi/hawala).

3\. Get a recommendation for a safe, regulated way to send money.

The goal is to reduce financial loss and legal risk for a population that is frequently targeted precisely because good information is hard to access.

**## 4. Real-World Impact**

\- Bangladesh is one of the world's largest recipients of remittances, and remittance income is a major contributor to household welfare and the national economy.

\- A large share of that flow still moves through informal, unregulated hundi/hawala channels — which regulators (Bangladesh Bank, BFIU, FATF) explicitly flag as vulnerable to fraud and money laundering.

\- Even a small improvement in the number of people who verify a rate or a channel before sending money translates into real money saved and real fraud prevented, at population scale.

**## 5. Why This Needs AI**

This isn't a problem a static FAQ page or a simple form can solve, because the right answer depends on combining several different, constantly-changing kinds of information:

\- **\*\*Live data\*\*** — exchange rates change daily; a hardcoded answer would be wrong within hours.

\- **\*\*Authoritative but dense source material\*\*** — financial regulations and AML reports are long, technical documents; most users won't read a 100-page FATF report themselves.

\- **\*\*Judgment under ambiguity\*\*** — "is this offer a scam?" doesn't have a lookup-table answer; it requires reasoning over the user's specific description against known fraud patterns.

An LLM-based multi-agent system, grounded in live search and a real regulatory knowledge base (RAG), is well suited to exactly this kind of reasoning — which a simple chatbot with no external grounding could not do reliably.

**## 6. Architecture**

\`\`\`

User query (text or screenshot)

        │

        ▼

   Router Agent  ──classifies intent──▶ rate | scam | channel | general

        │

   ┌────┴────┬─────────┬──────────┐

   ▼         ▼         ▼          ▼

 Rate       Scam     Channel   General

 Agent      Agent     Agent     Agent

(search)   (RAG)   (RAG+search) (LLM)

   │         │         │          │

   └────┬────┴─────────┴──────────┘

        ▼

  Response Aggregator

        │

        ▼

  Final structured answer

\`\`\`

**\*\*Agents\*\***

\- **\*\*Router Agent\*\*** — an LLM call that classifies the user's query into \`rate\`, \`scam\`, \`channel\`, or \`general\`.

\- **\*\*Rate Comparator Agent\*\*** — uses Tavily web search (search grounding) to answer live exchange-rate questions.

\- **\*\*Scam Detector Agent\*\*** — retrieves relevant chunks from the RAG knowledge base (Bangladesh AML law, BFIU circulars, FATF hawala/hundi reports) to assess whether a described channel or offer looks fraudulent.

\- **\*\*Channel Advisor Agent\*\*** — combines RAG + web search to recommend regulated, legal transfer channels.

\- **\*\*General Agent\*\*** — a fallback for anything outside the above three categories.

\- **\*\*Response Aggregator\*\*** — formats the selected agent's output into one consistent structured response for the frontend.

**\*\*OCR → Scam Agent integration\*\***

A user can upload a screenshot of a suspicious message or offer. The backend runs OCR (Tesseract) on it, and the extracted text is passed directly into the Scam Detector Agent for analysis — so OCR output is actually consumed by the reasoning pipeline, not just displayed as raw text.

**\*\*Resilience\*\***

All LLM calls go through a primary/fallback wrapper (\`app/llm.py\`): Google Gemini is tried first, and the system automatically falls back to Groq if Gemini is unavailable or rate-limited, so a single provider hiccup doesn't take the whole app down.

**## 7. Project Tree**

\`\`\`

remitguard/

├── .gitignore

├── README.md

├── backend/

│   ├── .env.example

│   ├── requirements.txt

│   ├── test\_rate\_agent.py

│   ├── test\_router.py

│   ├── test\_graph.py

│   └── app/

│       ├── main.py              # FastAPI app — routes: /health, /chat, /ocr, /analyze-screenshot

│       ├── config.py             # Settings loaded from .env (pydantic-settings)

│       ├── llm.py                # Primary (Gemini) / fallback (Groq) LLM wrapper

│       ├── graph.py               # LangGraph orchestration: router → agent → aggregator

│       ├── agents/

│       │   ├── router\_agent.py    # Classifies intent

│       │   ├── rate\_agent.py      # Exchange rate lookup (Tavily search)

│       │   ├── scam\_agent.py      # Scam/legality analysis (RAG)

│       │   ├── channel\_agent.py   # Safe channel recommendation (RAG + search)

│       │   ├── general\_agent.py   # Fallback for out-of-scope queries

│       │   └── aggregator.py      # Combines agent output into the final response

│       ├── tools/

│       │   ├── search\_tool.py         # Tavily search grounding

│       │   └── vectorstore\_tool.py    # Chroma retrieval

│       └── rag/

│           ├── ingest.py          # Chunks + embeds documents into Chroma

│           └── data/              # Source PDFs / TXT (regulatory documents)

└── frontend/

    ├── package.json

    └── src/

        ├── App.jsx                # Chat UI + screenshot upload

        ├── App.css

        └── index.css

\`\`\`

**## 8. How to Run This Project (Beginner-Friendly)**

This guide assumes no prior setup — follow it top to bottom.

**### Prerequisites**

Install these first if you don't already have them:

\- **\*\*Python 3.10+\*\*** — [python.org/downloads]\(https\://www\.python.org/downloads/)

\- **\*\*Node.js 18+\*\*** (includes npm) — [nodejs.org]\(https\://nodejs.org/)

\- **\*\*Git\*\*** — [git-scm.com]\(https\://git-scm.com/)

\- **\*\*Tesseract OCR\*\*** (needed for the screenshot-scam-check feature):

  - Windows: download the installer from [UB-Mannheim's Tesseract build]\(https\://github.com/UB-Mannheim/tesseract/wiki) and install it (default path \`C:\Program Files\Tesseract-OCR\tesseract.exe\`)

  - Mac: \`brew install tesseract\`

  - Linux: \`sudo apt install tesseract-ocr\`

**### Step 1 — Get the code**

\`\`\`bash

git clone \<your-repo-url>

cd remitguard

\`\`\`

**### Step 2 — Get free API keys**

You'll need free accounts (no credit card required) at:

\- [Google AI Studio]\(https\://aistudio.google.com/app/apikey) → \`GOOGLE\_API\_KEY\` (primary LLM)

\- [Groq]\(https\://console.groq.com/keys) → \`GROQ\_API\_KEY\` (fallback LLM)

\- [Tavily]\(https\://tavily.com) → \`TAVILY\_API\_KEY\` (web search)

\- [LangSmith]\(https\://smith.langchain.com) → \`LANGCHAIN\_API\_KEY\` / \`LANGSMITH\_API\_KEY\` (tracing)

**### Step 3 — Backend setup**

\`\`\`bash

cd backend

python -m venv venv

\# Windows:

venv\Scripts\activate

\# Mac/Linux:

source venv/bin/activate

pip install -r requirements.txt

\`\`\`

Copy \`.env.example\` to \`.env\` and fill in the keys from Step 2:

\`\`\`bash

cp .env.example .env        # Windows: copy .env.example .env

\`\`\`

Build the RAG knowledge base (only needs to be done once, or whenever documents in \`app/rag/data/\` change):

\`\`\`bash

python -m app.rag.ingest

\`\`\`

Start the backend server:

\`\`\`bash

uvicorn app.main\:app --reload

\`\`\`

Leave this terminal running. Visit \`http\://127.0.0.1:8000/health\` — you should see \`{"status": "ok", ...}\`.

**### Step 4 — Frontend setup**

Open a **\*\*new\*\*** terminal:

\`\`\`bash

cd remitguard/frontend

npm install

npm run dev

\`\`\`

Open the URL it prints (usually \`http\://127.0.0.1:5173\`) in your browser.

**### Step 5 — Try it out**

\- Ask a rate question: *\*"What's the USD to BDT rate via bKash today?"\**

\- Ask a scam question: *\*"Is it safe to send money through hundi to save on fees?"\**

\- Upload a screenshot of a suspicious offer using the "Upload screenshot" button.

**### Common issues**

\| Problem | Fix |

\|---|---|

\| \`ModuleNotFoundError\` | Run \`pip install -r requirements.txt\` again inside the activated venv |

\| \`ValidationError\` on startup | A required key is missing from \`.env\` — check against \`.env.example\` |

\| \`429 RESOURCE\_EXHAUSTED\` during ingest | You've hit Gemini's free-tier rate limit — this project uses local HuggingFace embeddings instead, so this shouldn't occur unless you've changed \`ingest.py\` |

\| \`tesseract is not installed or in your PATH\` | Install Tesseract (see Prerequisites) and set \`TESSERACT\_CMD\` in \`.env\` to its install path |

\| CORS error in browser console | Make sure the backend is running on port 8000 and the frontend on 5173 |

**## 9. Environment Variables**

See \`backend/.env.example\` for the full list. Never commit \`.env\` — it's already excluded via \`.gitignore\`.

\`\`\`

GOOGLE\_API\_KEY=

GROQ\_API\_KEY=

TAVILY\_API\_KEY=

LANGCHAIN\_TRACING\_V2=true

LANGCHAIN\_API\_KEY=

LANGCHAIN\_PROJECT=remitguard

LANGSMITH\_TRACING=true

LANGSMITH\_API\_KEY=

LANGSMITH\_ENDPOINT=https\://api.smith.langchain.com

LANGSMITH\_PROJECT=remitguard

APP\_ENV=development

\# Optional — only needed if Tesseract isn't on your system PATH

TESSERACT\_CMD=

\`\`\`

**## 10. RAG Knowledge Base**

The Scam Detector and Channel Advisor agents retrieve from a Chroma vector store built from real regulatory documents:

\- Bangladesh Bank foreign exchange / remittance circulars

\- Bangladesh Money Laundering Prevention Act (2015) & Rules (2019)

\- BFIU circulars and Annual Report

\- APG Bangladesh Mutual Evaluation Report

\- FATF reports on hawala/hundi and underground banking

Documents live in \`backend/app/rag/data/\`. \`ingest.py\` chunks them (1200 characters, 150 overlap), embeds them locally with \`sentence-transformers/all-MiniLM-L6-v2\` (no API calls, no rate limits), and stores them in a persistent Chroma collection at \`backend/app/rag/chroma\_db/\`.

**## 11. Tech Stack**

\| Layer | Technology |

\|---|---|

\| Frontend | React (Vite) |

\| Backend | FastAPI |

\| Agent orchestration | LangGraph |

\| Primary LLM | Google Gemini (\`langchain-google-genai\`) |

\| Fallback LLM | Groq |

\| Embeddings | HuggingFace \`sentence-transformers/all-MiniLM-L6-v2\` (local) |

\| Vector database | ChromaDB |

\| Internet search / grounding | Tavily |

\| OCR | Tesseract (\`pytesseract\`) |

\| Tracing | LangSmith |

**## 12. LangSmith Tracing**

Every agent call, tool call, and LLM invocation is traced to LangSmith under the \`remitguard\` project once \`LANGSMITH\_TRACING=true\` and a valid \`LANGSMITH\_API\_KEY\` are set in \`.env\`. Representative trace links demonstrating router → agent → retrieval/search → aggregator execution are provided in the Submission Links section above.

**## 13. Requirements Coverage

RemitGuard covers the major project requirements as follows:

| Requirement | RemitGuard Implementation |
|---|---|
| Real-world problem | Remittance safety, exchange-rate verification, scam detection, and safe-channel guidance |
| Front-end | React + Vite chat interface with screenshot upload |
| Back-end | FastAPI |
| Structured AI workflow | LangGraph Router → specialized Agent → Aggregator |
| Multiple agents | Router, Rate Comparator, Scam Detector, Channel Advisor, General Agent |
| Internet Search | Tavily search tool for current/external information |
| Search grounding | Retrieved web information is supplied to the relevant agent/LLM |
| OCR | Tesseract OCR for uploaded screenshots |
| RAG | Regulatory/scam knowledge base with document retrieval |
| Vector database | ChromaDB |
| Embeddings | Local `sentence-transformers/all-MiniLM-L6-v2` |
| LangSmith | Tracing for agent, tool, retrieval, and LLM execution |
| Environment security | API keys stored in `.env`, not committed to GitHub |
| Documentation | Setup, architecture, workflow, RAG, tech stack, and submission links documented here |

### Final Submission Checklist

- [ ] GitHub repository is public/accessible to the evaluator
- [ ] `.env` and API keys are **not** committed
- [ ] YouTube presentation link added above
- [ ] LangSmith trace links added above
- [ ] GitHub repository link added above
- [ ] Front-end demo works
- [ ] Rate Agent works
- [ ] Scam Detector + RAG works
- [ ] Channel Advisor works
- [ ] OCR works
- [ ] LangGraph end-to-end workflow works

## 14. Disclaimer**

RemitGuard provides informational guidance only. It does not replace advice from a bank or a licensed money transfer operator, and users should always independently verify details before sending money.