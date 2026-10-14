import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export default function Account({ user, onDeleted, onBack }) {
  const [count, setCount] = useState(null);
  const [confirming, setConfirming] = useState(false);
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch("/api/documents")
      .then((d) => setCount(d.documents.length))
      .catch(() => {});
  }, []);

  async function remove(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await apiFetch("/api/me/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      onDeleted(); // this screen is replaced, so there is nothing more to update here
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  function cancel() {
    setConfirming(false);
    setPassword("");
    setError("");
  }

  return (
    <section className="account">
      <div className="result-top">
        <div>
          <span className="eyebrow">Your account</span>
          <h2 className="result-title">Account</h2>
        </div>
        <button className="btn ghost" onClick={onBack}>
          ← Back
        </button>
      </div>

      <div className="card">
        <span className="term-label">Signed in as</span>
        <p className="account-email">{user.email}</p>
        <p className="muted-note">
          {count === null
            ? "Loading…"
            : count === 0
            ? "You have no saved documents."
            : `You have ${count} saved ${count === 1 ? "document" : "documents"}.`}
        </p>
      </div>

      <div className="card danger-zone">
        <h3 className="section-title">Delete my account</h3>
        <p>
          This permanently deletes your account, every document you have analysed,
          and all of your chat conversations. It cannot be undone.
        </p>

        {!confirming ? (
          <button className="btn danger" onClick={() => setConfirming(true)}>
            Delete my account
          </button>
        ) : (
          <form onSubmit={remove} className="danger-form">
            <label>
              Enter your password to confirm
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                autoFocus
                required
              />
            </label>

            {error && <div className="error-box">{error}</div>}

            <div className="danger-actions">
              <button className="btn danger" type="submit" disabled={busy || !password}>
                {busy ? "Deleting…" : "Permanently delete everything"}
              </button>
              <button className="btn ghost" type="button" onClick={cancel} disabled={busy}>
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </section>
  );
}