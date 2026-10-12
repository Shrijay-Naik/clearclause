import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from retrieval import domain_query, select_excerpts

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    max_retries=3,  # the library waits and retries when we hit a rate limit
    timeout=90,
)
MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

# How much document text we send per request. Groq's free plan allows about
# 8,000 tokens per minute (input + output), so these are kept modest.
ANALYSIS_BUDGET = 12000
CHAT_BUDGET = 9000

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

PARTIAL_ANALYSIS_NOTE = (
    "\nIMPORTANT: this is a long document, so you are shown only selected excerpts. "
    "Parts marked [... omitted ...] were not shown to you. Base everything only on the "
    "excerpts. Never say that something is missing or not mentioned in the document, "
    "because it may be in the omitted parts, and return an empty list for any "
    '"missing" field.\n'
)

PARTIAL_CHAT_NOTE = (
    "\nThis is a long document. You are shown only the parts that look most relevant "
    "to the question; parts marked [... omitted ...] were not shown. If the answer is "
    "not in the parts shown, say you could not find it in the relevant sections and "
    "suggest checking the full document. Do not say the document does not mention it.\n"
)
OCR_NOTE = (
    "\nNOTE: this text was read from a scanned image by OCR, so it may contain "
    "misread characters, odd line breaks and wrong digits. Be careful with amounts, "
    "percentages and dates: if a figure looks unclear or inconsistent, say that it "
    "looks unclear instead of guessing.\n"
)


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


def _is_too_large(e: Exception) -> bool:
    # HTTP 413 = the request is bigger than the plan allows
    return getattr(e, "status_code", None) == 413


def _run_analysis(
    excerpt: str, partial: bool, domain: dict, all_domains, ocr: bool = False
) -> dict:
    checklist = "\n".join(f"- {item}" for item in domain["risk_checklist"])
    key_terms = ", ".join(domain["key_term_hints"])

    # When the AI sees only excerpts it cannot know what is truly missing,
    # so we don't ask for the "missing" section at all.
    prompt_domain = domain
    if partial:
        prompt_domain = {
            **domain,
            "extra_sections": [
                s for s in domain.get("extra_sections", []) if s != "missing"
            ],
        }

    system_prompt = (
        f"{domain['role']}\n\n"
        "Explain everything for someone with no legal, medical or financial background. "
        "You are not a lawyer, doctor or financial advisor; this is general information, "
        "not professional advice.\n\n"
        f"The person reading your explanation is the {domain['reader']}.\n"
        f"Key terms worth extracting when present: {key_terms}.\n\n"
        f"Rules you must always follow:\n{guardrail_text(domain)}\n\n"
        f"Pay special attention to these risks:\n{checklist}\n"
        f"{PARTIAL_ANALYSIS_NOTE if partial else ''}"
        f"{OCR_NOTE if ocr else ''}"
        f"{build_output_format(prompt_domain, all_domains)}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document:\n\n{excerpt}"},
        ],
    )

    analysis = json.loads(response.choices[0].message.content)
    if not isinstance(analysis, dict):
        raise ValueError("The AI returned an unexpected format.")

    if partial:
        analysis["missing"] = []  # enforced here, in case the AI adds it anyway

    return analysis


def analyze_document(
    text: str, domain: dict, all_domains: dict | None = None, ocr: bool = False
) -> dict:
    budget = ANALYSIS_BUDGET
    query = domain_query(domain)

    for attempt in range(2):
        excerpt, share, partial = select_excerpts(text, query, budget)
        try:
            analysis = _run_analysis(excerpt, partial, domain, all_domains, ocr)
            break
        except Exception as e:
            # Too big for the plan: try once more with half the text
            if attempt == 0 and _is_too_large(e):
                budget //= 2
                continue
            raise

    # Saved with the analysis, so the interface can tell the user what was covered
    analysis["coverage"] = {
        "partial": partial,
        "percent": round(share * 100),
        "total_chars": len(text),
    }
    return analysis


def chat_with_document(text: str, domain: dict, history: list, question: str) -> str:
    # Follow-up questions ("and if I'm two months late?") need the previous question too
    last_user = next((m["content"] for m in reversed(history) if m["role"] == "user"), "")
    query = f"{question} {last_user}"
    budget = CHAT_BUDGET

    for attempt in range(2):
        excerpt, _share, partial = select_excerpts(text, query, budget, keep_start=False)

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
            f"{guardrail_text(domain)}\n"
            f"{PARTIAL_CHAT_NOTE if partial else ''}\n"
            f"DOCUMENT:\n{excerpt}"
        )

        messages = [{"role": "system", "content": system_prompt}]
        messages += history[-6:]  # only the most recent messages, to stay within limits
        messages.append({"role": "user", "content": question})

        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=0.3,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 0 and _is_too_large(e):
                budget //= 2
                continue
            raise