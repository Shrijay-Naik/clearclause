import { useEffect, useState } from "react";
import UploadZone from "./components/UploadZone";
import Loading from "./components/Loading";
import ResultView from "./components/ResultView";
import AuthScreen from "./components/AuthScreen";
import History from "./components/History";
import WakeUp from "./components/WakeUp";
import Footer from "./components/Footer";
import PrivacyModal from "./components/PrivacyModal";
import {
  apiFetch,
  clearToken,
  getToken,
  setToken,
  setUnauthorizedHandler,
} from "./api";

const MAX_MB = 10;

export default function App() {
  const [user, setUser] = useState(null);
  const [booting, setBooting] = useState(true); // waiting for the backend
  const [view, setView] = useState("home"); // home | history
  const [domains, setDomains] = useState([]);
  const [domain, setDomain] = useState("finance");
  const [status, setStatus] = useState("checking"); // checking | ok | bad
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [showPrivacy, setShowPrivacy] = useState(false);

  function logout() {
    clearToken();
    setUser(null);
    setResult(null);
    setView("home");
    setError("");
  }

  useEffect(() => {
    setUnauthorizedHandler(logout);
    let cancelled = false;

    async function boot() {
      // Free hosting sleeps when idle, so keep retrying for about 2 minutes
      for (let attempt = 0; attempt < 40 && !cancelled; attempt++) {
        try {
          const data = await apiFetch("/api/domains");
          if (cancelled) return;
          setDomains(data.domains);
          setStatus("ok");

          // Only now that the backend is awake do we check the saved login
          if (getToken()) {
            try {
              setUser(await apiFetch("/api/me"));
            } catch {
              // A 401 already logs the user out; other errors just show the login screen
            }
          }
          setBooting(false);
          return;
        } catch {
          await new Promise((r) => setTimeout(r, 3000));
        }
      }
      if (!cancelled) {
        setStatus("bad");
        setBooting(false);
      }
    }

    boot();
    return () => {
      cancelled = true;
    };
  }, []);

  function handleAuth(data) {
    setToken(data.access_token);
    setUser(data.user);
    setView("home");
  }

  async function handleFile(file) {
    setError("");

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Please choose a PDF file.");
      return;
    }
    if (file.size > MAX_MB * 1024 * 1024) {
      setError(`That file is larger than ${MAX_MB} MB.`);
      return;
    }

    setLoading(true);
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("domain", domain);

      const data = await apiFetch("/api/analyze", { method: "POST", body: form });
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function goNew() {
    setResult(null);
    setError("");
    setView("home");
  }

  function openFromHistory(data) {
    setResult(data);
    setView("home");
  }

  const currentDomain = domains.find((d) => d.id === domain);

  const statusText = {
    checking: "Connecting…",
    ok: "Backend connected",
    bad: "Backend offline",
  }[status];

  if (booting) {
    return (
      <div className="page">
        <div className="container">
          <header className="header">
            <div className="brand">
              <span className="brand-mark">§</span>
              ClearClause
            </div>
          </header>
          <WakeUp />
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="container">
        <header className="header">
          <div className="brand">
            <span className="brand-mark">§</span>
            ClearClause
          </div>

          <div className="header-right">
            <div className="status">
              <span className={`dot ${status === "checking" ? "" : status}`} />
              {statusText}
            </div>

            {user && (
              <>
                <button className="nav-link" onClick={goNew}>
                  New analysis
                </button>
                <button className="nav-link" onClick={() => setView("history")}>
                  My documents
                </button>
                <span className="user-email">{user.email}</span>
                <button className="nav-link" onClick={logout}>
                  Log out
                </button>
              </>
            )}
          </div>
        </header>

        {!user ? (
          <AuthScreen
            onAuth={handleAuth}
            onOpenPrivacy={() => setShowPrivacy(true)}
          />
        ) : view === "history" ? (
          <History onOpen={openFromHistory} onNew={goNew} />
        ) : result ? (
          <ResultView
            result={result}
            onReset={goNew}
            onUpdate={setResult}
            domainInfo={domains.find((d) => d.id === result.domain)}
          />
        ) : (
          <>
            <section className="hero">
              <span className="eyebrow">AI contract reader</span>
              <h1>
                Understand what you sign, <em>in plain English.</em>
              </h1>
              <p>
                Upload a contract or legal document. Get a clear summary, the
                risky clauses flagged, and answers to your questions.
              </p>

              <div className="chips">
                {domains.map((d) => (
                  <button
                    key={d.id}
                    className={`chip ${domain === d.id ? "active" : ""}`}
                    onClick={() => setDomain(d.id)}
                  >
                    {d.name}
                  </button>
                ))}
              </div>
            </section>

            <section className="upload-area">
              {currentDomain && (
                <p className="domain-note">
                  <strong>{currentDomain.name}</strong> works best with:{" "}
                  {currentDomain.accepts}
                </p>
              )}
              {currentDomain?.upload_warning && (
                <div className="warn-box">{currentDomain.upload_warning}</div>
              )}

              {loading ? <Loading /> : <UploadZone onFile={handleFile} disabled={loading} />}
              {error && <div className="error-box">{error}</div>}
              <p className="upload-note">
                Your file is sent to an AI service for analysis. Please don't
                upload documents containing ID or bank account numbers.
              </p>
            </section>
          </>
        )}

        <Footer onOpenPrivacy={() => setShowPrivacy(true)} />
      </div>

      {showPrivacy && <PrivacyModal onClose={() => setShowPrivacy(false)} />}
    </div>
  );
}