export default function Footer({ onOpenPrivacy }) {
  return (
    <footer className="footer">
      <p>
        ClearClause gives general information, not legal or financial advice.{" "}
        <button type="button" className="link" onClick={onOpenPrivacy}>
          Privacy &amp; terms
        </button>
      </p>
    </footer>
  );
}