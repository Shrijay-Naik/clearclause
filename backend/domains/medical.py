CONFIG = {
    "id": "medical",
    "name": "Medical",
    "description": "Health insurance policies, hospital consent forms and discharge summaries",
    "accepts": "Health insurance policies, hospital consent and admission forms, medical bills and discharge summaries",
    "role": (
        "You are an expert in health insurance policies and hospital paperwork such as "
        "consent forms, admission forms, estimates, bills and discharge summaries. You "
        "explain what a document says in plain language, so patients understand what they "
        "are agreeing to and what is covered. You explain documents; you do not give "
        "medical advice."
    ),
    "reader": "patient",
    "example_document_type": "Health Insurance Policy",
    "disclaimer": "This explains the document, not your health. It is not medical, legal or insurance advice. Ask your doctor about your health and your insurer about your claim.",
    "features": {"chat": True},
    "extra_sections": ["questions_to_ask", "missing"],
    "sections": {
        "risks": {"title": "Watch out for"},
        "questions_to_ask": {
            "title": "Ask the insurer or hospital",
            "note": "Good questions to ask before you sign or file a claim.",
        },
        "missing": {
            "title": "Not mentioned in this document",
            "note": "Documents of this type usually cover these. Ask for them in writing.",
        },
    },
    "upload_warning": "Health records are very sensitive. Use a sample or edited copy: remove your name, patient ID, Aadhaar, policy number and phone number before uploading.",
    "guardrails": [
        "Never diagnose, never suggest treatments, and never comment on medicines or doses. Explain what the document's words mean, and tell the person to ask their doctor what it means for their health.",
        "Never say whether a test result or a condition is serious or normal for the person.",
        "If the person describes symptoms or an emergency, tell them to contact a doctor or local emergency services right away instead of answering.",
        "Never promise that a claim will or will not be approved; explain only what the document says.",
    ],
    "risk_checklist": [
        "Waiting periods: the initial waiting period, the waiting period for pre-existing diseases, and waiting periods for specific illnesses",
        "Exclusions: treatments, conditions or situations the policy will not pay for",
        "Room rent limits and 'proportionate deduction' that can reduce the whole claim",
        "Sub-limits on specific treatments, and caps on the total amount payable (sum insured)",
        "Co-payment and deductible: the share of the bill the patient must pay",
        "Items that are not payable, such as consumables and administrative charges",
        "Claim process: deadlines to inform the insurer, cashless vs reimbursement, documents needed",
        "Pre-existing conditions: the duty to disclose them, and claim rejection or cancellation for non-disclosure",
        "Renewal: premium increases, age-based loading, and conditions for renewing or cancelling",
        "Hospital forms: consent to 'any necessary' treatment without details, and consent to share medical records",
        "Financial responsibility: advance deposits, estimates that can change, and the patient paying for uncovered amounts",
        "Waivers: giving up the right to complain or claim, discharge against medical advice, and limits on the hospital's liability",
    ],
    "key_term_hints": [
        "Type of document",
        "Sum insured or coverage amount",
        "Premium",
        "Waiting periods",
        "Co-payment or deductible",
        "Main exclusions",
        "Claim deadline",
        "Room rent limit",
    ],
    "chat_suggestions": [
        "What is not covered?",
        "How do I make a claim, and by when?",
        "What does the waiting period mean for me?",
        "Explain the medical terms in this document",
    ],
    "glossary": [
        {
            "term": "Premium",
            "aliases": ["premium", "premiums"],
            "meaning": "The amount you pay, monthly or yearly, to keep the policy active.",
        },
        {
            "term": "Sum insured",
            "aliases": ["sum insured", "sum assured", "coverage amount", "cover amount"],
            "meaning": "The maximum amount the insurer will pay in a policy year.",
        },
        {
            "term": "Deductible",
            "aliases": ["deductible"],
            "meaning": "A fixed amount you pay yourself before the insurer starts paying.",
        },
        {
            "term": "Co-payment",
            "aliases": ["co-payment", "copayment", "co-pay", "copay"],
            "meaning": "A percentage of every claim that you pay yourself.",
        },
        {
            "term": "Waiting period",
            "aliases": ["waiting period"],
            "meaning": "A time after buying the policy during which some or all claims are not paid.",
        },
        {
            "term": "Pre-existing condition",
            "aliases": ["pre-existing", "preexisting", "pre existing"],
            "meaning": "A health condition you already had before buying the policy. These usually have a longer waiting period or are excluded, and you must disclose them honestly.",
        },
        {
            "term": "Exclusion",
            "aliases": ["exclusion", "exclusions", "excluded"],
            "meaning": "Something the policy specifically does not pay for.",
        },
        {
            "term": "Sub-limit",
            "aliases": ["sub-limit", "sublimit", "sub limit"],
            "meaning": "A cap on how much is paid for a specific item, such as a procedure or room, even if your total sum insured is higher.",
        },
        {
            "term": "Room rent limit",
            "aliases": ["room rent", "room rent cap"],
            "meaning": "A cap on the daily room charge the policy covers. Choosing a costlier room can also reduce other payments (see proportionate deduction).",
        },
        {
            "term": "Proportionate deduction",
            "aliases": ["proportionate deduction", "proportionately", "proportionate"],
            "meaning": "If your room costs more than the limit, many other charges are cut by the same proportion, not just the room charge.",
        },
        {
            "term": "Cashless",
            "aliases": ["cashless", "cash-less"],
            "meaning": "The insurer pays the hospital directly, usually only at network hospitals and with prior approval.",
        },
        {
            "term": "Reimbursement",
            "aliases": ["reimbursement", "reimburse"],
            "meaning": "You pay the hospital first and then claim the money back from the insurer with documents.",
        },
        {
            "term": "TPA (third-party administrator)",
            "aliases": ["tpa", "third party administrator", "third-party administrator"],
            "meaning": "A company that handles claims on behalf of the insurer.",
        },
        {
            "term": "Network hospital",
            "aliases": ["network hospital", "network provider", "empanelled"],
            "meaning": "A hospital that has an agreement with the insurer for cashless treatment.",
        },
        {
            "term": "Informed consent",
            "aliases": ["informed consent", "consent"],
            "meaning": "Your agreement to a treatment after the risks, benefits and alternatives have been explained to you. Make sure you understand it before signing.",
        },
        {
            "term": "Discharge summary",
            "aliases": ["discharge summary", "discharge"],
            "meaning": "A report written when you leave the hospital, describing why you were admitted, what was done and what to do next.",
        },
        {
            "term": "Discharge against medical advice",
            "aliases": ["against medical advice", "lama", "dama"],
            "meaning": "Leaving the hospital when the doctor advises you to stay. Forms for this often limit the hospital's responsibility.",
        },
        {
            "term": "Diagnosis",
            "aliases": ["diagnosis", "diagnosed"],
            "meaning": "The doctor's conclusion about what condition you have.",
        },
        {
            "term": "Free-look period",
            "aliases": ["free look", "free-look"],
            "meaning": "A short period after buying a policy during which you can cancel it and get a refund, usually after small deductions.",
        },
        {
            "term": "Portability",
            "aliases": ["portability", "port the policy"],
            "meaning": "Moving your policy to another insurer while keeping benefits you have already built up, such as waiting periods served.",
        },
    ],
}