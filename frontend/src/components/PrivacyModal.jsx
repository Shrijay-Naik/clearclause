import { useEffect } from "react";

export default function PrivacyModal({ onClose }) {
  // Pressing Escape closes the pop-up
  useEffect(() => {
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        onClick={(e) => e.stopPropagation()}
      >
        <h2>Privacy &amp; terms</h2>
        <p className="modal-sub">The short, honest version.</p>

        <h4>What this is</h4>
        <p>
          ClearClause is a student capstone project. It explains contracts in
          plain English and flags clauses that may be risky. It is{" "}
          <strong>not legal or financial advice</strong>, and AI can make mistakes.
          Before you sign anything important, check it with a qualified
          professional.
        </p>

        <h4>What we store</h4>
        <ul>
          <li>Your email address</li>
          <li>Your password, saved only in scrambled (hashed) form</li>
          <li>
            For each document you upload: the file name, the text extracted from
            it, and the AI analysis
          </li>
        </ul>

        <h4>Who can see your documents</h4>
        <p>
          Other users cannot see your documents. To produce summaries and answer
          your questions, the document text is sent to a third-party AI service
          (Groq). The app does not add extra encryption to stored document text.
        </p>

        <h4>Your control</h4>
        <p>
          You can delete any document at any time from <em>My documents</em>.
          Account deletion is not available yet.
        </p>

        <h4>Please avoid uploading</h4>
        <p>
          ID numbers (such as Aadhaar or PAN), bank account numbers, or card
          numbers. Remove these details from the file before uploading.
        </p>

        <h4>Good to know</h4>
        <p>
          This is a free demo on free hosting, so the service can be slow or
          unavailable at times.
        </p>

        <button className="btn" onClick={onClose}>
          Got it
        </button>
      </div>
    </div>
  );
}