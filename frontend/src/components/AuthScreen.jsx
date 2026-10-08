import { useState } from "react";
import { apiFetch } from "../api";

export default function AuthScreen({ onAuth, onOpenPrivacy }) {
  const [mode, setMode] = useState("login"); // login | signup
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [agreed, setAgreed] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const isSignup = mode === "signup";

  function switchMode() {
    setMode(isSignup ? "login" : "signup");
    setError("");
  }

  async function submit(e) {
    e.preventDefault();
    setError("");

    if (isSignup && password.length < 8) {
      setError("Your password needs at least 8 characters.");
      return;
    }
    if (isSignup && !agreed) {
      setError("Please tick the box to confirm you've read the privacy note.");
      return;
    }

    setBusy(true);
    try {
      let data;
      if (isSignup) {
        data = await apiFetch("/api/auth/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });
      } else {
        // The login endpoint expects a form, with the email in the "username" field
        data = await apiFetch("/api/auth/login", {
          method: "POST",
          body: new URLSearchParams({ username: email, password }),
        });
      }
      onAuth(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="auth-wrap">
      <div className="auth-intro">
        <span className="eyebrow">AI contract reader</span>
        <h1>
          Understand what you sign, <em>in plain English.</em>
        </h1>
        <p>
          Create a free account to analyse contracts, spot risky clauses,
          and keep every document in one place.
        </p>
      </div>

      <form className="card auth-card" onSubmit={submit}>
        <h2>{isSignup ? "Create your account" : "Welcome back"}</h2>

        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            autoComplete="email"
            required
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={isSignup ? "At least 8 characters" : "Your password"}
            autoComplete={isSignup ? "new-password" : "current-password"}
            required
          />
        </label>

        {isSignup && (
          <label className="consent">
            <input
              type="checkbox"
              checked={agreed}
              onChange={(e) => setAgreed(e.target.checked)}
            />
            <span>
              I understand this gives general information, not legal or financial
              advice, and I've read the{" "}
              <button type="button" className="link" onClick={onOpenPrivacy}>
                privacy note
              </button>
              .
            </span>
          </label>
        )}

        {error && <div className="error-box">{error}</div>}

        <button className="btn wide" type="submit" disabled={busy}>
          {busy ? "Please wait…" : isSignup ? "Create account" : "Log in"}
        </button>

        <p className="switch">
          {isSignup ? "Already have an account?" : "New to ClearClause?"}{" "}
          <button type="button" className="link" onClick={switchMode}>
            {isSignup ? "Log in" : "Create an account"}
          </button>
        </p>
      </form>
    </section>
  );
}