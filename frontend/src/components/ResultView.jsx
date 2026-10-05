import { useState } from "react";
import Chat from "./Chat";

const ORDER = { high: 0, medium: 1, low: 2 };

function normalize(sev) {
  const s = String(sev || "").toLowerCase();
  return ORDER[s] !== undefined ? s : "low";
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

export default function ResultView({ result, onReset, api }) {
  const a = result.analysis;
  const keyTerms = a.key_terms || [];
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

      <section className="block">
        <div className="risk-header">
          <h3 className="section-title">Watch out for</h3>
          <div className="risk-counts">
            <span className="count high">{count("high")} high</span>
            <span className="count medium">{count("medium")} medium</span>
            <span className="count low">{count("low")} low</span>
          </div>
        </div>

        {risks.length === 0 ? (
          <div className="card">No risky clauses were found.</div>
        ) : (
          <div className="risk-list">
            {risks.map((r, i) => (
              <RiskCard key={i} item={r} defaultOpen={i === 0} />
            ))}
          </div>
        )}
        <div className="chat-wrap">
          <Chat api={api} documentId={result.document_id} />
        </div>
        <p className="disclaimer">
          ClearClause gives general information, not legal or financial advice.
          For important decisions, consult a qualified professional.
        </p>
      </section>
    </div>
  );
}