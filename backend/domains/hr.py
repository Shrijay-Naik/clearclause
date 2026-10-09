CONFIG = {
    "id": "hr",
    "name": "HR & Employment",
    "description": "Offer letters, employment contracts, NDAs and service agreements",
    "accepts": "Offer letters, appointment letters, employment contracts, NDAs, internship and service-bond agreements",
    "role": (
        "You are an expert in employment documents such as offer letters, appointment "
        "letters, employment contracts, NDAs, non-compete clauses, internship agreements "
        "and service-bond agreements. You help employees understand what they are about "
        "to sign before they accept a job."
    ),
    "reader": "employee",
    "example_document_type": "Employment Offer Letter",
    "disclaimer": "General information, not legal advice. Employment rules differ by country and state.",
    # No chat for HR: these documents are short and decision-focused, so a
    # pre-signing checklist helps more. To switch chat on, set "chat": True
    # and add a "chat_suggestions" list.
    "features": {"chat": False},
    "extra_sections": ["questions_to_ask", "missing"],
    "sections": {
        "risks": {"title": "Clauses to look at closely"},
        "questions_to_ask": {
            "title": "Ask HR before you sign",
            "note": "Try to get the answers in writing, ideally in the final document.",
        },
        "missing": {
            "title": "Not mentioned in this document",
            "note": "Employment documents usually cover these. Ask for them in writing.",
        },
    },
    "upload_warning": "Remove Aadhaar, PAN, bank account numbers and your home address before uploading.",
    "guardrails": [
        "Never tell the person to accept or reject the offer, or to resign; explain the terms and the risks.",
        "Do not state that a clause is illegal or unenforceable. Say it may be worth checking with a lawyer or the labour department.",
    ],
    "risk_checklist": [
        "Notice period length, whether it is the same for employer and employee, and any buy-out or pay-in-lieu terms",
        "Service bond, minimum service period, or training-cost recovery if the employee leaves early",
        "Clawback of joining bonus, relocation or sign-on payments",
        "Probation length, how it can be extended, and different terms during probation",
        "Salary structure: fixed vs variable pay, whether bonuses are guaranteed or discretionary, and the gap between total package (CTC) and take-home pay",
        "Non-compete, non-solicit or exclusivity clauses after leaving, or bans on side work during employment",
        "Intellectual property clauses that claim work done in the employee's own time or unrelated to the job",
        "Confidentiality (NDA) scope and how long it lasts",
        "Termination terms: dismissal without notice or cause, one-sided rights, and what happens to unpaid dues",
        "Employer keeping original certificates or documents",
        "Offer conditions: background verification, withdrawal of the offer, and the right to change role, location or terms later",
        "Vague terms such as 'as per company policy' where the policy is not attached",
        "Dispute resolution: forced arbitration or courts in a distant city",
    ],
    "key_term_hints": [
        "Job title and department",
        "Salary or total package (CTC)",
        "Joining date and work location",
        "Probation period",
        "Notice period",
        "Service bond or minimum stay",
        "Non-compete or confidentiality terms",
    ],
    "glossary": [
        {
            "term": "CTC (cost to company)",
            "aliases": ["ctc", "cost to company", "total package"],
            "meaning": "The total yearly amount the company spends on you, including benefits and employer contributions. Your take-home pay is usually lower.",
        },
        {
            "term": "Take-home salary",
            "aliases": ["take-home", "take home", "in-hand", "in hand", "net salary", "net pay"],
            "meaning": "What reaches your bank account each month after deductions such as tax and provident fund.",
        },
        {
            "term": "Probation",
            "aliases": ["probation", "probationary"],
            "meaning": "A trial period at the start of a job. Notice, leave and other terms are often different during this time.",
        },
        {
            "term": "Notice period",
            "aliases": ["notice period", "period of notice"],
            "meaning": "How long you or the employer must give notice before ending the job. You usually keep working and being paid during this time.",
        },
        {
            "term": "Notice buy-out",
            "aliases": ["buy-out", "buyout", "buy out", "pay in lieu", "in lieu of notice"],
            "meaning": "Paying money instead of working through the notice period. Check who may use this option and how the amount is calculated.",
        },
        {
            "term": "Service bond",
            "aliases": ["service bond", "bond period", "minimum service", "training bond", "minimum stay"],
            "meaning": "An agreement that you will stay for a minimum time, or repay money (such as training costs) if you leave early.",
        },
        {
            "term": "Clawback",
            "aliases": ["clawback", "claw back", "claw-back"],
            "meaning": "The company's right to take back money it paid you earlier, such as a joining bonus, if you leave too soon.",
        },
        {
            "term": "Non-compete",
            "aliases": ["non-compete", "non compete", "noncompete"],
            "meaning": "A promise not to work for a competitor, or start a competing business, for some time after you leave. Whether it can be enforced depends on local law.",
        },
        {
            "term": "Non-solicit",
            "aliases": ["non-solicit", "non solicit", "nonsolicit"],
            "meaning": "A promise not to take the company's clients or employees with you when you leave.",
        },
        {
            "term": "Confidentiality / NDA",
            "aliases": ["confidentiality", "non-disclosure", "nda", "confidential information"],
            "meaning": "A promise to keep certain company information secret, sometimes even after you leave.",
        },
        {
            "term": "Intellectual property (IP)",
            "aliases": ["intellectual property", "work product", "inventions"],
            "meaning": "Things you create, such as code, designs or writing. IP clauses say who owns them. Check whether they cover only work for the company or also your own time.",
        },
        {
            "term": "Variable pay",
            "aliases": ["variable pay", "performance bonus", "incentive"],
            "meaning": "Pay that depends on performance or company results and may not be guaranteed.",
        },
        {
            "term": "Discretionary",
            "aliases": ["discretion", "discretionary", "sole discretion"],
            "meaning": "The company decides, with no obligation. If a bonus is discretionary, you may not be able to demand it.",
        },
        {
            "term": "Provident fund (PF)",
            "aliases": ["provident fund", "epf", "pf contribution"],
            "meaning": "A retirement savings scheme where both you and the employer contribute part of your salary.",
        },
        {
            "term": "Gratuity",
            "aliases": ["gratuity"],
            "meaning": "A lump sum paid by the employer for long service, usually after a minimum number of years with the company.",
        },
        {
            "term": "Background verification",
            "aliases": ["background verification", "background check", "bgv", "reference check"],
            "meaning": "Checks on your past jobs, education or records. Offers are often conditional on passing them.",
        },
        {
            "term": "Full and final settlement",
            "aliases": ["full and final", "relieving letter", "experience letter"],
            "meaning": "The last payment of your dues when you leave. Relieving and experience letters are the documents you should receive at exit.",
        },
        {
            "term": "Arbitration",
            "aliases": ["arbitration", "arbitrator"],
            "meaning": "Settling a dispute privately through an arbitrator instead of a court. Check where it takes place and who chooses the arbitrator.",
        },
        {
            "term": "Jurisdiction",
            "aliases": ["jurisdiction"],
            "meaning": "Which courts, and which city's or country's laws, will apply if there is a dispute.",
        },
    ],
}