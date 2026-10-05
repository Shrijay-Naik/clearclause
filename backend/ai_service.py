import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

# Keeps us within free-tier limits. We'll handle long documents properly later.
MAX_CHARS = 20000

OUTPUT_FORMAT = """
Respond with ONLY valid JSON in exactly this shape:
{
  "document_type": "short name of the document, e.g. Personal Loan Agreement",
  "summary": "3 to 5 sentences in simple language a teenager could understand",
  "key_terms": [
    {"label": "e.g. Interest rate", "value": "e.g. 12% per year, compounded monthly"}
  ],
  "risky_clauses": [
    {
      "clause": "a short quote or description of the clause",
      "severity": "high, medium or low",
      "why_risky": "why this could hurt the borrower",
      "plain_english": "what the clause actually means in simple words",
      "suggestion": "what the person could ask for or check before signing"
    }
  ]
}
Order risky_clauses from most to least severe. Only use information from the document.
If something is not in the document, do not invent it.
"""


def analyze_document(text: str, domain: dict) -> dict:
    checklist = "\n".join(f"- {item}" for item in domain["risk_checklist"])

    system_prompt = (
        f"{domain['role']}\n\n"
        "Explain everything for someone with no legal or financial background. "
        "You are not a lawyer and this is general information, not legal advice.\n\n"
        f"Pay special attention to these risks:\n{checklist}\n"
        f"{OUTPUT_FORMAT}"
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
        "You are answering questions about the document below.\n"
        "Rules:\n"
        "- Answer ONLY using the document. If the answer is not in it, say so clearly "
        "and do not guess.\n"
        "- Use simple language a teenager could understand.\n"
        "- Mention the relevant clause or section number when you can.\n"
        "- Keep answers short, and use a quick example with numbers when it helps.\n"
        "- Use the same currency symbol as the document. If the document has none, "
        "do not assume one; write plain numbers.\n"
        "- You are not a lawyer; this is general information, not legal advice.\n\n"
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