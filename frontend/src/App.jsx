import { useState } from "react";
import "./index.css";
import "./App.css";

const EXAMPLES = [
  "Is Western Union safe for sending $500 abroad?",
  "Someone offered a much better rate over WhatsApp — legit?",
  "Best way to send money to family in Nigeria?",
];

const STATUS_META = {
  safe: { label: "Looks safe", tone: "safe" },
  ok: { label: "Looks safe", tone: "safe" },
  scam: { label: "Possible scam", tone: "danger" },
  fraud: { label: "Possible scam", tone: "danger" },
  warning: { label: "Proceed with caution", tone: "warn" },
  caution: { label: "Proceed with caution", tone: "warn" },
  error: { label: "Something went wrong", tone: "danger" },
  info: { label: "Good to know", tone: "info" },
};

function getStatus(route) {
  const key = (route || "").toLowerCase();
  return STATUS_META[key] || { label: route || "Result", tone: "info" };
}

function formatResponse(text) {
  if (!text) return [];

  const lines = text.split("\n");
  const sections = [];
  let current = null;

  lines.forEach((line) => {
    const clean = line.trim();

    if (clean.startsWith("###")) {
      if (current) sections.push(current);
      current = {
        title: clean.replace(/^###\s*/, "").replace(/\*\*/g, ""),
        content: [],
      };
    } else if (current) {
      if (clean) current.content.push(clean);
    } else if (clean) {
      current = { title: "Summary", content: [clean] };
    }
  });

  if (current) sections.push(current);
  return sections;
}

function IconShield(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" {...props}>
      <path
        d="M12 3l7 3v5c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
      <path
        d="M9 12l2 2 4-4"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconExchange(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" {...props}>
      <path
        d="M4 8h13m0 0l-3.5-3.5M17 8l-3.5 3.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M20 16H7m0 0l3.5-3.5M7 16l3.5 3.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconAlert(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" {...props}>
      <path
        d="M12 4l9 16H3l9-16z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
      <path d="M12 10v4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
      <circle cx="12" cy="17" r="0.9" fill="currentColor" />
    </svg>
  );
}

function IconBank(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" {...props}>
      <path
        d="M4 10l8-5 8 5M5 10v8m4-8v8m6-8v8m4-8v8M3 20h18"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconSend(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" {...props}>
      <path
        d="M4 12l16-8-6 16-3-6-7-2z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function HeroArt() {
  return (
    <svg
      viewBox="0 0 320 260"
      className="hero-art"
      width="280"
      height="228"
      role="img"
      aria-label="A route from one place to another, checked safe along the way"
    >
      <defs>
        <linearGradient id="rg-brand" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#146c82" />
          <stop offset="100%" stopColor="#0a3f4e" />
        </linearGradient>
      </defs>

      <path
        d="M40 190C90 130 130 90 170 90c50 0 40 60 90 60"
        stroke="#c9dade"
        strokeWidth="2.5"
        strokeDasharray="1 9"
        strokeLinecap="round"
        fill="none"
      />

      <circle cx="40" cy="190" r="9" fill="#dd9a35" />
      <circle cx="260" cy="150" r="9" fill="url(#rg-brand)" />

      <g transform="translate(140,48)">
        <path
          d="M30 0l30 13v22c0 20-13 34-30 40-17-6-30-20-30-40V13L30 0z"
          fill="url(#rg-brand)"
        />
        <path
          d="M18 34l9 9 17-18"
          stroke="white"
          strokeWidth="4"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
      </g>
    </svg>
  );
}

function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setResult(data);
    } catch (error) {
      setResult({ route: "error", response: error.message });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sections = result ? formatResponse(result.response) : [];
  const status = result ? getStatus(result.route) : null;

  return (
    <div className="app">
      <header className="site-header">
        <div className="brand">
          <span className="brand-mark">
            Remit<span>Guard</span>
          </span>
          <span className="brand-tagline">Know before you send</span>
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div className="hero-copy">
            <h1>Before you send, ask.</h1>
            <p>
              Describe your transfer, or paste a message you're unsure about.
              RemitGuard checks it against current rates, common scam
              patterns, and legal transfer channels, then explains what it
              finds in plain language.
            </p>

            <div className="check-panel">
              <textarea
                placeholder="Ask a question, or paste a message you're unsure about…"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                rows="4"
                aria-label="Your remittance question"
              />

              <div className="check-panel-footer">
                <span className="hint">
                  <kbd>Enter</kbd> to check &middot; <kbd>Shift</kbd>+<kbd>Enter</kbd> for a new line
                </span>

                <button
                  className="check-button"
                  onClick={sendMessage}
                  disabled={loading || !message.trim()}
                >
                  {loading ? (
                    <>
                      Checking
                      <span aria-hidden="true">
                        <span className="spinner-dot" />
                        <span className="spinner-dot" />
                        <span className="spinner-dot" />
                      </span>
                    </>
                  ) : (
                    <>
                      <IconSend width="16" height="16" />
                      Check my transfer
                    </>
                  )}
                </button>
              </div>

              <div className="examples">
                <p>Not sure where to start? Try one of these:</p>
                <div className="example-chips">
                  {EXAMPLES.map((example) => (
                    <button key={example} onClick={() => setMessage(example)} type="button">
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <HeroArt />
        </section>

        {result && (
          <section className="result-panel" aria-live="polite">
            <div className="result-panel-header">
              <h2>What we found</h2>
              <span className={`pill pill--${status.tone}`}>
                {status.tone === "danger" && <IconAlert width="14" height="14" />}
                {status.tone === "safe" && <IconShield width="14" height="14" />}
                {status.label}
              </span>
            </div>

            <div className="answer-sections">
              {sections.map((section, index) => (
                <div className="answer-section" key={index}>
                  <h3>{section.title}</h3>
                  {section.content.map((line, i) => (
                    <p key={i}>{line.replace(/\*\*/g, "").replace(/^\*\s*/, "")}</p>
                  ))}
                </div>
              ))}
            </div>

            <p className="result-disclaimer">
              This is AI-generated guidance. Always confirm details with your
              bank or a licensed money transfer operator before sending money.
            </p>
          </section>
        )}

        <section className="features">
          <div className="feature" style={{ "--feature-accent": "var(--primary)" }}>
            <IconExchange className="icon-badge" />
            <h3>Exchange rates</h3>
            <p>See today's rates before you commit, so no one can quietly shortchange you.</p>
          </div>

          <div className="feature" style={{ "--feature-accent": "var(--danger)" }}>
            <IconAlert className="icon-badge" />
            <h3>Scam detection</h3>
            <p>Paste a suspicious message or offer to see if it matches known scam patterns.</p>
          </div>

          <div className="feature" style={{ "--feature-accent": "var(--gold)" }}>
            <IconBank className="icon-badge" />
            <h3>Safe channels</h3>
            <p>Compare legal, regulated ways to send money — banks, operators, and mobile transfers.</p>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <p>RemitGuard helps you double-check a transfer.</p>
        <p>It doesn't replace advice from your bank or a licensed money transfer operator.</p>
      </footer>
    </div>
  );
}

export default App;
