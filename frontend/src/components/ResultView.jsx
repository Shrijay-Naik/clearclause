import { useState } from "react";
import Chat from "./Chat";

const ORDER = { high: 0, medium: 1, low: 2 };

function normalize(sev) {
  const s = String(sev || "").toLowerCase();
  return ORDER[s] !== undefined ? s : "low";
}

// The AI usually returns plain text, but be forgiving if it returns an object
function asText(x) {
  if (typeof x === "string") return x;
  return x?.what || x?.question || x?.text || "";
}

function RiskCard({ item, defaultOpen }) {
  const [open, setOpen] = useState(defaultOpen);
  const sev = normalize(item.severity);

  return (
    <div className={`risk ${sev} ${open ? "open" : ""}`}>
      <button className="risk-head" onClick={() => setOpen(!open)}>
        <span className={`badge ${sev}`}>{sev}</span>
        <span className="risk-title">{item.clause}</span>
        <span className="chevron">{open ? "−" : "+"}</span>
      </button>

      {open && (
        <div className="risk-body">
          <div className="risk-block plain">
            <h4>In plain English</h4>
            <p>{item.plain_english}</p>
          </div>
          <div className="risk-block">
            <h4>Why it's risky</h4>
            <p>{item.why_risky}</p>
          </div>
          <div className="risk-block tip">
            <h4>What you can do</h4>
            <p>{item.suggestion}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ResultView({ result, onReset, domainInfo }) {
  const a = result.analysis;
  const sections = domainInfo?.sections || {};
  const title = (key, fallback) => sections[key]?.title || fallback;
  const note = (key) => sections[key]?.note;
  const showChat = domainInfo?.features?.chat !== false;

  const keyTerms = a.key_terms || [];
  const glossary = result.glossary || [];
  const actionItems = a.action_items || [];
  const questions = a.questions_to_ask || [];
  const missing = a.missing || [];
  const risks = [...(a.risky_clauses || [])].sort(
    (x, y) => ORDER[normalize(x.severity)] - ORDER[normalize(y.severity)]
  );
  const count = (s) => risks.filter((r) => normalize(r.severity) === s).length;

  return (
    <div className="result">
      <div className="result-top">
        <div>
          <span className="eyebrow">{a.document_type}</span>
          <h2 className="result-title">{result.filename}</h2>
          <p className="result-meta">
            {domainInfo ? `${domainInfo.name} · ` : ""}
            {result.pages} {result.pages === 1 ? "page" : "pages"} analysed
          </p>
        </div>
        <button className="btn ghost" onClick={onReset}>
          ← New document
        </button>
      </div>

      <section className="card summary">
        <h3 className="section-title">The short version</h3>
        <p className="summary-text">{a.summary}</p>
      </section>

      {keyTerms.length > 0 && (
        <section className="block">
          <h3 className="section-title">Key terms</h3>
          <div className="terms-grid">
            {keyTerms.map((t, i) => (
              <div className="term" key={i}>
                <span className="term-label">{t.label}</span>
                <span className="term-value">{t.value}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {actionItems.length > 0 && (
        <section className="block">
          <h3 className="section-title">{title("action_items", "What to do next")}</h3>
          {note("action_items") && <p className="section-note">{note("action_items")}</p>}
          <div className="action-list">
            {actionItems.map((it, i) => (
              <div className="action" key={i}>
                {it?.when && <span className="action-when">{it.when}</span>}
                <span className="action-what">{asText(it)}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="block">
        <div className="risk-header">
          <h3 className="section-title">{title("risks", "Watch out for")}</h3>
          <div className="risk-counts">
            <span className="count high">{count("high")} high</span>
            <span className="count medium">{count("medium")} medium</span>
            <span className="count low">{count("low")} low</span>
          </div>
        </div>

        {risks.length === 0 ? (
          <div className="card">Nothing risky was found.</div>
        ) : (
          <div className="risk-list">
            {risks.map((r, i) => (
              <RiskCard key={i} item={r} defaultOpen={i === 0} />
            ))}
          </div>
        )}
      </section>

      {missing.length > 0 && (
        <section className="block">
          <h3 className="section-title">{title("missing", "Not mentioned in this document")}</h3>
          {note("missing") && <p className="section-note">{note("missing")}</p>}
          <div className="card">
            <ul className="plain-list">
              {missing.map((m, i) => (
                <li key={i}>{asText(m)}</li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {questions.length > 0 && (
        <section className="block">
          <h3 className="section-title">{title("questions_to_ask", "Questions to ask")}</h3>
          {note("questions_to_ask") && (
            <p className="section-note">{note("questions_to_ask")}</p>
          )}
          <div className="card">
            <ol className="plain-list">
              {questions.map((q, i) => (
                <li key={i}>{asText(q)}</li>
              ))}
            </ol>
          </div>
        </section>
      )}

      {glossary.length > 0 && (
        <div className="glossary-wrap">
          <h3 className="section-title">Terms explained</h3>
          <p className="glossary-sub">
            Words found in your document, in plain English. Tap to open.
          </p>
          <div className="glossary">
            {glossary.map((g) => (
              <details className="gloss" key={g.term}>
                <summary>{g.term}</summary>
                <p>{g.meaning}</p>
              </details>
            ))}
          </div>
        </div>
      )}

      {showChat && (
        <div className="chat-wrap">
          <Chat
            documentId={result.document_id}
            suggestions={domainInfo?.chat_suggestions}
          />
        </div>
      )}

      <p className="disclaimer">
        {domainInfo?.disclaimer || "General information, not professional advice."}{" "}
        For important decisions, consult a qualified professional.
      </p>
    </div>
  );
}