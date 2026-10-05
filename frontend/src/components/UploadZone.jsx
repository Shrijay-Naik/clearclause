import { useRef, useState } from "react";

export default function UploadZone({ onFile, disabled }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  function pick(file) {
    if (file) onFile(file);
  }

  return (
    <div
      className={`dropzone ${dragging ? "dragging" : ""}`}
      onClick={() => !disabled && inputRef.current.click()}
      onDragOver={(e) => {
        e.preventDefault();
        if (!disabled) setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        if (!disabled) pick(e.dataTransfer.files[0]);
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf,.pdf"
        hidden
        onChange={(e) => {
          pick(e.target.files[0]);
          e.target.value = "";
        }}
      />

      <div className="drop-icon">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" />
          <path d="M14 3v5h5" />
          <path d="M12 17v-6M9.5 13.5 12 11l2.5 2.5" />
        </svg>
      </div>
      <h3>Drop your contract here</h3>
      <p>or click to browse · PDF only · up to 10 MB</p>
    </div>
  );
}