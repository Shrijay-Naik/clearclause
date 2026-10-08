import re

from .finance import CONFIG as finance

# To add a domain: create a file like hr.py with a CONFIG dictionary,
# import it above, and add it to this list.
_ALL = [finance]

_REQUIRED = {
    "id": str,
    "name": str,
    "description": str,
    "accepts": str,
    "role": str,
    "reader": str,
    "example_document_type": str,
    "disclaimer": str,
    "risk_checklist": list,
    "key_term_hints": list,
    "chat_suggestions": list,
    "glossary": list,
}


def _validate(cfg: dict) -> None:
    name = cfg.get("id", "<unknown>")
    for field, kind in _REQUIRED.items():
        if field not in cfg:
            raise ValueError(f"Domain '{name}' is missing the field '{field}'")
        if not isinstance(cfg[field], kind) or not cfg[field]:
            raise ValueError(
                f"Domain '{name}': '{field}' must be a non-empty {kind.__name__}"
            )
    for i, entry in enumerate(cfg["glossary"]):
        for key in ("term", "aliases", "meaning"):
            if key not in entry:
                raise ValueError(
                    f"Domain '{name}': glossary entry {i + 1} is missing '{key}'"
                )


for _cfg in _ALL:
    _validate(_cfg)

DOMAINS = {cfg["id"]: cfg for cfg in _ALL}


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