export default function OcrProgress({ progress, cancelling, onCancel }) {
  let label = "Getting the reader ready. The first time can take a minute…";
  let fraction = 0;

  if (progress?.stage === "reading") {
    label =
      progress.total > 1
        ? `Reading page ${progress.page} of ${progress.total}…`
        : "Reading the text…";
    fraction = (progress.page - 1 + (progress.fraction || 0)) / progress.total;
  }
  const pct = Math.round(fraction * 100);

  return (
    <div className="ocr card">
      <h3>Reading your scan</h3>
      <p>
        This is an image rather than typed text, so it is read on your device.
        Only the text it finds is sent for analysis.
      </p>
      <div className="bar">
        <span style={{ width: `${Math.max(pct, 4)}%` }} />
      </div>
      <p className="ocr-label">
        {cancelling ? "Stopping…" : label}
        {!cancelling && pct > 0 ? ` ${pct}%` : ""}
      </p>
      <button className="btn ghost" onClick={onCancel} disabled={cancelling}>
        Cancel
      </button>
    </div>
  );
}