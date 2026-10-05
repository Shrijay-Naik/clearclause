import { useEffect, useState } from "react";

const MESSAGES = [
  "Reading your document…",
  "Finding the key terms…",
  "Checking for risky clauses…",
  "Translating into plain English…",
];

export default function Loading() {
  const [i, setI] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setI((n) => (n + 1) % MESSAGES.length), 2500);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading">
      <div className="spinner" />
      <p>{MESSAGES[i]}</p>
    </div>
  );
}