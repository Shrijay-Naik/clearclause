import { useEffect, useRef, useState } from "react";
import { apiFetch } from "../api";

const SUGGESTIONS = [
  "What happens if I miss a payment?",
  "Can I repay this early without a fee?",
  "Which clause should I negotiate first?",
  "Explain this to me like I'm 15",
];

// Turns **bold** text from the AI into real bold text
function renderInline(text) {
  return text.split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
    part.startsWith("**") && part.endsWith("**") ? (
      <strong key={i}>{part.slice(2, -2)}</strong>
    ) : (
      part
    )
  );
}

export default function Chat({ documentId, suggestions, initialMessages }) {
  // The server keeps the conversation, so earlier messages arrive with the document
  const [messages, setMessages] = useState(initialMessages || []);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const boxRef = useRef(null);

  // Keep the newest message in view (scrolls only the chat box, not the page)
  useEffect(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = boxRef.current.scrollHeight;
    }
  }, [messages, busy]);

  async function send(text) {
    const question = text.trim();
    if (!question || busy) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setBusy(true);

    try {
      // No history is sent: the server remembers the conversation
      const data = await apiFetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ document_id: documentId, question }),
      });
      setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: e.message, error: true },
      ]);
    } finally {
      setBusy(false);
    }
  }

  async function clearChat() {
    if (!window.confirm("Clear this conversation? This can't be undone.")) return;
    try {
      await apiFetch(`/api/documents/${documentId}/messages`, { method: "DELETE" });
      setMessages([]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: e.message, error: true },
      ]);
    }
  }

  const hasSaved = messages.some((m) => !m.error);

  return (
    <div className="chat card">
      <div className="chat-head">
        <div>
          <h3 className="section-title">Ask about this document</h3>
          <p>Answers come only from your document. If it isn't covered, I'll say so.</p>
        </div>
        {hasSaved && (
          <button className="link-btn" onClick={clearChat} disabled={busy}>
            Clear chat
          </button>
        )}
      </div>

      <div className="chat-box" ref={boxRef}>
        {messages.length === 0 && (
          <div className="suggestions">
            {(suggestions && suggestions.length ? suggestions : SUGGESTIONS).map((s) => (
              <button key={s} className="suggestion" onClick={() => send(s)}>
                {s}
              </button>
            ))}
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`bubble-row ${m.role}`}>
            <div className={`bubble ${m.role} ${m.error ? "error" : ""}`}>
              {renderInline(m.content)}
            </div>
          </div>
        ))}

        {busy && (
          <div className="bubble-row assistant">
            <div className="bubble assistant typing">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}
      </div>

      <form
        className="chat-input"
        onSubmit={(e) => {
          e.preventDefault();
          send(input);
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything, e.g. “What if I'm two months late?”"
          disabled={busy}
          maxLength={2000}
        />
        <button type="submit" className="send" disabled={busy || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}