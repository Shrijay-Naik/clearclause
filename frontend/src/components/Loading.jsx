import { useEffect, useState } from "react";

const MESSAGES = [
  "Reading your document…",
  "Finding the key terms…",
  "Checking for risky clauses…",
  "Translating into plain English…",
];

export default function Loading() {
  const [i, setI] = useState(0);
  const [slow, setSlow] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => setI((n) => (n + 1) % MESSAGES.length), 2500);
    const slowTimer = setTimeout(() => setSlow(true), 15000);
    return () => {
      clearInterval(timer);
      clearTimeout(slowTimer);
    };
  }, []);

  return (
    <div className="loading">
      <div className="spinner" />
      <p>{MESSAGES[i]}</p>
      {slow && (
        <p className="slow-note">
          Still working. If the server was asleep, the first request can take up to
          a minute.
        </p>
      )}
    </div>
  );
}