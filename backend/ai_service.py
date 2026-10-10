import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

# Keeps us within free-tier limits. We'll handle long documents properly later.
MAX_CHARS = 20000

# Optional result sections a domain can switch on with "extra_sections".
# If you add one here, also add its name to KNOWN_SECTIONS in domains/__init__.py
EXTRA_SECTIONS = {
    "action_items": {
        "shape": '"action_items": [{"what": "something the person must do or be aware of", "when": "the deadline, date or time limit exactly as written in the document, or Not stated"}]',
        "rule": "For action_items, copy every date and time limit exactly as written. Never calculate or guess a date. Use an empty list if there are none.",
    },
    "questions_to_ask": {
        "shape": '"questions_to_ask": ["a specific question the person should ask before agreeing, based on this document"]',
        "rule": "For questions_to_ask, give 3 to 6 specific, practical questions.",
    },
    "missing": {
        "shape": '"missing": ["something normally found in this kind of document that is NOT mentioned in it"]',
        "rule": "For missing, list at most 5 items, and only things that are genuinely absent from the document.",
    },
}

OUTPUT_FORMAT = """
Respond with ONLY valid JSON in exactly this shape:
{
  "document_type": "short name of the document, e.g. __EXAMPLE__",
  "detected_domain": "the category this document actually belongs to, judged only from its content. Exactly one of: __CHOICES__",
  "summary": "3 to 5 sentences in simple language a teenager could understand",
  "key_terms": [
    {"label": "short label", "value": "what the document says about it"}
  ],
  "risky_clauses": [
    {
      "clause": "a short quote or description of the clause",
      "severity": "high, medium or low",
      "why_risky": "why this could hurt the __READER__",
      "plain_english": "what the clause actually means in simple words",
      "suggestion": "what the __READER__ could ask for or check next"
    }
  ]__EXTRA_SHAPE__
}
Order risky_clauses from most to least severe. Only use information from the document.
If something is not in the document, do not invent it.
Use the same currency symbols as the document. Never assume a currency that is not written there.
Fill in detected_domain honestly from the document's content, even if it differs from the category you were asked to analyse it under.
__EXTRA_RULES__
"""


def domain_choices(all_domains: dict | None, domain: dict) -> str:
    pool = all_domains or {domain["id"]: domain}
    parts = [f'"{d["id"]}" ({d["accepts"]})' for d in pool.values()]
    parts.append('"other" (none of these)')
    return "; ".join(parts)


def build_output_format(domain: dict, all_domains: dict | None = None) -> str:
    names = domain.get("extra_sections", [])
    shape = "".join(",\n  " + EXTRA_SECTIONS[n]["shape"] for n in names)
    rules = "\n".join(EXTRA_SECTIONS[n]["rule"] for n in names)
    return (
        OUTPUT_FORMAT.replace("__EXAMPLE__", domain["example_document_type"])
        .replace("__CHOICES__", domain_choices(all_domains, domain))
        .replace("__READER__", domain["reader"])
        .replace("__EXTRA_SHAPE__", shape)
        .replace("__EXTRA_RULES__", rules)
    )


def guardrail_text(domain: dict) -> str:
    return "\n".join(f"- {g}" for g in domain["guardrails"])


def analyze_document(text: str, domain: dict, all_domains: dict | None = None) -> dict:
    checklist = "\n".join(f"- {item}" for item in domain["risk_checklist"])
    key_terms = ", ".join(domain["key_term_hints"])

    system_prompt = (
        f"{domain['role']}\n\n"
        "Explain everything for someone with no legal, medical or financial background. "
        "You are not a lawyer, doctor or financial advisor; this is general information, "
        "not professional advice.\n\n"
        f"The person reading your explanation is the {domain['reader']}.\n"
        f"Key terms worth extracting when present: {key_terms}.\n\n"
        f"Rules you must always follow:\n{guardrail_text(domain)}\n\n"
        f"Pay special attention to these risks:\n{checklist}\n"
        f"{build_output_format(domain, all_domains)}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document:\n\n{text[:MAX_CHARS]}"},
        ],
    )

    return json.loads(response.choices[0].message.content)


def chat_with_document(text: str, domain: dict, history: list, question: str) -> str:
    system_prompt = (
        f"{domain['role']}\n\n"
        f"The person asking is the {domain['reader']}. "
        "You are answering questions about the document below.\n"
        "Rules:\n"
        "- Answer ONLY using the document. If the answer is not in it, say so clearly "
        "and do not guess.\n"
        "- Use simple language a teenager could understand.\n"
        "- Mention the relevant clause or section number when you can.\n"
        "- Keep answers short, and use a quick example with numbers when it helps.\n"
        "- Use the same currency symbol as the document. If the document shows none, "
        "do not assume one; write plain numbers.\n"
        "- You are not a lawyer, doctor or financial advisor; this is general "
        "information, not professional advice.\n"
        f"{guardrail_text(domain)}\n\n"
        f"DOCUMENT:\n{text[:MAX_CHARS]}"
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages += history[-10:]  # only the last 10 messages, to stay within limits
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        messages=messages,
    )
    return response.choices[0].message.content