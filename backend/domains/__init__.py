import re

from .court import CONFIG as court
from .finance import CONFIG as finance
from .hr import CONFIG as hr
from .medical import CONFIG as medical

# To add a domain: create a file like hr.py with a CONFIG dictionary,
# import it above, and add it to this list.
_ALL = [finance, hr, medical, court]

# Optional result sections a domain can switch on with "extra_sections".
# Keep in sync with EXTRA_SECTIONS in ai_service.py.
KNOWN_SECTIONS = {"action_items", "questions_to_ask", "missing"}

_REQUIRED = {
    "id": str,
    "name": str,
    "description": str,
    "accepts": str,
    "role": str,
    "reader": str,
    "example_document_type": str,
    "disclaimer": str,
    "upload_warning": str,
    "risk_checklist": list,
    "key_term_hints": list,
    "glossary": list,
    "guardrails": list,
    "extra_sections": list,
    "features": dict,
    "sections": dict,
}
_ALLOW_EMPTY = {"extra_sections"}


def _validate(cfg: dict) -> None:
    name = cfg.get("id", "<unknown>")
    for field, kind in _REQUIRED.items():
        if field not in cfg:
            raise ValueError(f"Domain '{name}' is missing the field '{field}'")
        if not isinstance(cfg[field], kind):
            raise ValueError(f"Domain '{name}': '{field}' must be a {kind.__name__}")
        if field not in _ALLOW_EMPTY and not cfg[field]:
            raise ValueError(f"Domain '{name}': '{field}' must not be empty")

    for section in cfg["extra_sections"]:
        if section not in KNOWN_SECTIONS:
            raise ValueError(f"Domain '{name}': unknown extra section '{section}'")

    if "chat" not in cfg["features"]:
        raise ValueError(f"Domain '{name}': features must include 'chat' (True or False)")
    if cfg["features"]["chat"] and not cfg.get("chat_suggestions"):
        raise ValueError(f"Domain '{name}' has chat turned on, so it needs 'chat_suggestions'")

    for i, entry in enumerate(cfg["glossary"]):
        for key in ("term", "aliases", "meaning"):
            if key not in entry:
                raise ValueError(f"Domain '{name}': glossary entry {i + 1} is missing '{key}'")


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