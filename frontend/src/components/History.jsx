import { useEffect, useState } from "react";
import { apiFetch } from "../api";

// The server stores times in UTC; make sure the browser reads them that way
function formatDate(s) {
  const iso = /Z|[+-]\d\d:\d\d$/.test(s) ? s : s + "Z";
  return new Date(iso).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export default function History({ onOpen, onNew }) {
  const [docs, setDocs] = useState(null); // null = still loading
  const [error, setError] = useState("");
  const [openingId, setOpeningId] = useState(null);

  useEffect(() => {
    apiFetch("/api/documents")
      .then((d) => setDocs(d.documents))
      .catch((e) => {
        setError(e.message);
        setDocs([]);
      });
  }, []);

  async function open(id) {
    setError("");
    setOpeningId(id);
    try {
      const data = await apiFetch(`/api/documents/${id}`);
      onOpen(data);
    } catch (e) {
      setError(e.message);
      setOpeningId(null);
    }
  }

  async function remove(e, id) {
    e.stopPropagation();
    if (!window.confirm("Delete this document? This can't be undone.")) return;
    try {
      await apiFetch(`/api/documents/${id}`, { method: "DELETE" });
      setDocs((prev) => prev.filter((d) => d.document_id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="history">
      <div className="result-top">
        <div>
          <span className="eyebrow">Your library</span>
          <h2 className="result-title">My documents</h2>
        </div>
        <button className="btn" style={{ marginTop: 0 }} onClick={onNew}>
          + Analyse a document
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}

      {docs === null && <p className="muted-note">Loading…</p>}

      {docs && docs.length === 0 && !error && (
        <div className="card empty">
          <h3>Nothing here yet</h3>
          <p>Documents you analyse will be saved here, so you can come back to them.</p>
          <button className="btn" onClick={onNew}>
            Analyse your first document
          </button>
        </div>
      )}

      <div className="doc-list">
        {docs &&
          docs.map((d) => (
            <div
              key={d.document_id}
              className="doc-row"
              onClick={() => open(d.document_id)}
            >
              <div className="doc-icon">§</div>
              <div className="doc-info">
                <span className="doc-name">{d.filename}</span>
                <span className="doc-meta">
                  {d.document_type || "Document"} · {d.pages}{" "}
                  {d.pages === 1 ? "page" : "pages"} · {formatDate(d.created_at)}
                </span>
              </div>
              <span className="doc-open">
                {openingId === d.document_id ? "Opening…" : "Open →"}
              </span>
              <button
                className="doc-delete"
                title="Delete"
                onClick={(e) => remove(e, d.document_id)}
              >
                ✕
              </button>
            </div>
          ))}
      </div>
    </section>
  );
}