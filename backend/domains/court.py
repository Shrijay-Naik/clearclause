CONFIG = {
    "id": "court",
    "name": "Court & Legal Notices",
    "description": "Court notices, summons, orders, judgments and legal notices",
    "accepts": "Legal notices, court summons, orders and judgments, affidavits and petitions",
    "role": (
        "You are an expert in explaining court and legal documents such as summons, legal "
        "notices, orders, judgments, affidavits and petitions. You help ordinary people "
        "understand what a document says, what it requires them to do, and by when. You "
        "explain documents; you are not their lawyer."
    ),
    "reader": "party concerned",
    "example_document_type": "Legal Notice",
    "disclaimer": "General information, not legal advice. Court deadlines are strict, so confirm every date with the court or a qualified lawyer.",
    "features": {"chat": True},
    "extra_sections": ["action_items"],
    "sections": {
        "risks": {"title": "Points that need attention"},
        "action_items": {
            "title": "What you need to do, and by when",
            "note": "Dates are taken from the document and can be misread. Always confirm them with the court or a lawyer, because missing a deadline can have serious consequences.",
        },
    },
    "upload_warning": "Court papers often contain names, addresses and case details. Use a sample or edited copy, and remove ID numbers before uploading.",
    "guardrails": [
        "Never predict how a case will end or tell the person what their legal chances are.",
        "Never tell the person to ignore a notice or summons. If a document sets a deadline or hearing date, remind them to confirm it and to consider speaking to a lawyer.",
        "Copy dates and deadlines exactly as written; never calculate or guess a date.",
        "Do not assume which side the person is on unless the document makes it clear.",
    ],
    "risk_checklist": [
        "Deadlines to reply, appear in court or comply, and what happens if they are missed",
        "Hearing dates, the court, and the place or online link where the person must appear",
        "Orders that take effect automatically if the person does not respond, such as a decision made in their absence",
        "Money to be paid: amounts, interest, penalties, costs and the date they are due",
        "Orders to do or stop doing something (injunctions, stays, vacating property) and the penalty for ignoring them",
        "Statements the person is asked to confirm or admit that could be used against them",
        "Threats of further action in a legal notice, such as criminal proceedings or recovery of money",
        "Attachment of property, freezing of bank accounts or other enforcement steps",
        "Limits on the right to appeal, and the time allowed to appeal",
        "Unclear parties, case numbers or demands that need checking before responding",
    ],
    "key_term_hints": [
        "Court or authority",
        "Case number",
        "Parties (who is suing or accusing whom)",
        "Type of document",
        "Hearing or next date",
        "Order or relief",
        "Amount claimed, if any",
    ],
    "chat_suggestions": [
        "What is this document asking me to do?",
        "What happens if I don't reply by the deadline?",
        "Who are the parties and what is the dispute about?",
        "Explain the legal terms in this document",
    ],
    "glossary": [
        {
            "term": "Summons",
            "aliases": ["summons", "summon"],
            "meaning": "An official order to appear in court, or to respond to a case, at a stated time.",
        },
        {
            "term": "Legal notice",
            "aliases": ["legal notice", "demand notice"],
            "meaning": "A formal written warning sent before going to court, usually demanding that something be done by a deadline.",
        },
        {
            "term": "Plaintiff / complainant",
            "aliases": ["plaintiff", "complainant"],
            "meaning": "The person who starts a case or makes a complaint.",
        },
        {
            "term": "Defendant / respondent",
            "aliases": ["defendant", "respondent"],
            "meaning": "The person a case is brought against, who must respond.",
        },
        {
            "term": "Petitioner",
            "aliases": ["petitioner", "applicant"],
            "meaning": "The person who files a petition or application asking the court for something.",
        },
        {
            "term": "Accused",
            "aliases": ["accused"],
            "meaning": "A person charged with, or suspected of, a crime in a criminal case.",
        },
        {
            "term": "Interim order",
            "aliases": ["interim order", "interim relief", "interim"],
            "meaning": "A temporary order made while the case is still going on.",
        },
        {
            "term": "Ex-parte",
            "aliases": ["ex-parte", "ex parte", "exparte"],
            "meaning": "Decided or ordered with only one side present. If you do not appear, the court may decide without hearing you.",
        },
        {
            "term": "Adjournment",
            "aliases": ["adjourned", "adjournment"],
            "meaning": "Postponing a hearing to another date.",
        },
        {
            "term": "Injunction",
            "aliases": ["injunction"],
            "meaning": "A court order to do, or to stop doing, something.",
        },
        {
            "term": "Stay",
            "aliases": ["stay order", "stay of execution", "stayed"],
            "meaning": "A court order that pauses an action, or another order, for a time.",
        },
        {
            "term": "Decree",
            "aliases": ["decree"],
            "meaning": "The formal written order of a civil court that records its decision.",
        },
        {
            "term": "Judgment",
            "aliases": ["judgment", "judgement"],
            "meaning": "The court's reasoned decision in a case.",
        },
        {
            "term": "Affidavit",
            "aliases": ["affidavit"],
            "meaning": "A written statement of facts that you swear or affirm is true. False statements can lead to punishment.",
        },
        {
            "term": "Appeal",
            "aliases": ["appeal", "appellate"],
            "meaning": "Asking a higher court to review a decision. There is usually a strict time limit.",
        },
        {
            "term": "Jurisdiction",
            "aliases": ["jurisdiction"],
            "meaning": "The power of a particular court to hear a case, based on place, subject or amount.",
        },
        {
            "term": "Limitation period",
            "aliases": ["limitation period", "time-barred", "time barred"],
            "meaning": "The time limit within which a case or appeal must be filed. After it, the claim may be barred.",
        },
        {
            "term": "Written statement",
            "aliases": ["written statement"],
            "meaning": "The defendant's formal written reply to the plaintiff's claim.",
        },
        {
            "term": "Bail",
            "aliases": ["bail"],
            "meaning": "Temporary release of an accused person during a case, usually with conditions.",
        },
        {
            "term": "FIR",
            "aliases": ["fir", "first information report"],
            "meaning": "First Information Report: the written record police make when they receive information about a crime.",
        },
        {
            "term": "Contempt of court",
            "aliases": ["contempt"],
            "meaning": "Disobeying a court order or disrespecting the court, which can lead to penalties.",
        },
    ],
}