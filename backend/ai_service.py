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

# __EXAMPLE__ and __READER__ are filled in from the domain config
OUTPUT_FORMAT = """
Respond with ONLY valid JSON in exactly this shape:
{
  "document_type": "short name of the document, e.g. __EXAMPLE__",
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
      "suggestion": "what the __READER__ could ask for or check before agreeing"
    }
  ]
}
Order risky_clauses from most to least severe. Only use information from the document.
If something is not in the document, do not invent it.
Use the same currency symbols as the document. Never assume a currency that is not written there.
"""


def analyze_document(text: str, domain: dict) -> dict:
    checklist = "\n".join(f"- {item}" for item in domain["risk_checklist"])
    key_terms = ", ".join(domain["key_term_hints"])
    output_format = OUTPUT_FORMAT.replace(
        "__EXAMPLE__", domain["example_document_type"]
    ).replace("__READER__", domain["reader"])

    system_prompt = (
        f"{domain['role']}\n\n"
        "Explain everything for someone with no legal, medical or financial background. "
        "You are not a lawyer, doctor or financial advisor; this is general information, "
        "not professional advice.\n\n"
        f"The person reading your explanation is the {domain['reader']}.\n"
        f"Key terms worth extracting when present: {key_terms}.\n\n"
        f"Pay special attention to these risks:\n{checklist}\n"
        f"{output_format}"
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
        "information, not professional advice.\n\n"
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