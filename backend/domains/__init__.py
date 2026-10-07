import re

from .finance import CONFIG as finance

# To add a new domain later: create a file like legal.py and register it here.
DOMAINS = {
    "finance": finance,
}


def find_glossary(text: str, domain: dict) -> list:
    """Returns the glossary entries whose trigger words appear in the document."""
    found = []
    for entry in domain.get("glossary", []):
        for alias in entry["aliases"]:
            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            if re.search(pattern, text, re.IGNORECASE):
                found.append({"term": entry["term"], "meaning": entry["meaning"]})
                break
    return found