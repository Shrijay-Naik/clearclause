"""Finds the most relevant parts of a long document (keyword-based retrieval)."""
import math
import re
from collections import Counter

_WORD = re.compile(r"[a-z0-9][a-z0-9'\-]*")
_STOP = set(
    "the and for with that this from are was were been being have has had not but "
    "you your our their his her its they them will shall may can could would should "
    "must does did any all each other such than then there here which who whom "
    "into over under per also".split()
)
_HEADING = re.compile(
    r"^\s*(\d+(\.\d+)*[.)]\s|clause\b|section\b|article\b|schedule\b|annexure\b)",
    re.IGNORECASE,
)


def _words(text: str) -> list:
    return [w for w in _WORD.findall(text.lower()) if len(w) > 2 and w not in _STOP]


def split_chunks(text: str, target: int = 1500) -> list:
    """Cuts text into pieces of roughly `target` characters, preferring to
    start a new piece at a clause heading."""
    chunks, current, size = [], [], 0

    def flush():
        nonlocal current, size
        piece = "\n".join(current).strip()
        if piece:
            chunks.append(piece)
        current, size = [], 0

    for raw in text.splitlines():
        line = raw.rstrip()
        # A very long line (a PDF with no line breaks) is cut into slices
        slices = [line[i : i + target] for i in range(0, len(line), target)] or [""]
        for piece in slices:
            is_heading = bool(_HEADING.match(piece)) or (
                piece.isupper() and 3 < len(piece) < 80
            )
            if current and ((size >= target and is_heading) or size >= target * 1.4):
                flush()
            current.append(piece)
            size += len(piece) + 1
    flush()
    return chunks


def _scores(chunks: list, query: str) -> list:
    """BM25 relevance score of every chunk for the query."""
    terms = set(_words(query))
    docs = [Counter(_words(c)) for c in chunks]
    n = len(chunks)
    lengths = [sum(d.values()) or 1 for d in docs]
    avg = sum(lengths) / n if n else 1

    df = Counter()
    for d in docs:
        for t in terms:
            if t in d:
                df[t] += 1

    scores = []
    for d, length in zip(docs, lengths):
        s = 0.0
        for t in terms:
            tf = d.get(t, 0)
            if tf:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * length / avg))
        scores.append(s)
    return scores


def select_excerpts(text: str, query: str, budget: int, keep_start: bool = True):
    """Returns (text_to_send, share_of_document_included, was_shortened)."""
    if len(text) <= budget:
        return text, 1.0, False

    chunks = split_chunks(text)
    scores = _scores(chunks, query)
    order = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)

    chosen, used = set(), 0
    if keep_start:  # the opening usually names the parties, date and purpose
        chosen.add(0)
        used = len(chunks[0])
    for i in order:
        if i in chosen:
            continue
        if used + len(chunks[i]) + 2 > budget:
            continue
        chosen.add(i)
        used += len(chunks[i]) + 2

    parts, previous = [], -1
    for i in sorted(chosen):
        if i != previous + 1:
            parts.append("[... omitted ...]")
        parts.append(chunks[i])
        previous = i
    if previous < len(chunks) - 1:
        parts.append("[... omitted ...]")

    included = sum(len(chunks[i]) for i in chosen)
    total = sum(len(c) for c in chunks) or 1
    return "\n\n".join(parts), included / total, True


def domain_query(domain: dict) -> str:
    """Everything this domain cares about, used to pick the relevant parts."""
    parts = list(domain["risk_checklist"]) + list(domain["key_term_hints"])
    for entry in domain["glossary"]:
        parts.extend(entry["aliases"])
    return " ".join(parts)