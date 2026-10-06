import { useEffect, useState } from "react";

export default function WakeUp() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="wake card">
      <div className="spinner" />
      {seconds < 4 ? (
        <p>Connecting…</p>
      ) : (
        <>
          <h3>Waking up the server</h3>
          <p>
            This project runs on free hosting, which goes to sleep when nobody is
            using it. Starting up usually takes under a minute. Hang tight, it
            will continue by itself.
          </p>
          <p className="wake-timer">{seconds}s</p>
        </>
      )}
    </div>
  );
}