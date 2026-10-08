CONFIG = {
    "id": "finance",
    "name": "Finance",
    "description": "Loan agreements, credit card terms, insurance policies",
        "accepts": "Loan agreements, credit card terms, insurance policies",
    "reader": "borrower",
    "example_document_type": "Personal Loan Agreement",
    "disclaimer": "General information, not legal or financial advice.",
    "key_term_hints": [
        "Interest rate",
        "Loan amount",
        "Repayment period or monthly instalment",
        "Late payment penalty",
        "Fees and charges",
        "Collateral or guarantor",
    ],
    "chat_suggestions": [
        "What happens if I miss a payment?",
        "Can I repay this early without a fee?",
        "Which clause should I negotiate first?",
        "Explain this to me like I'm 15",
    ],
    "role": (
        "You are an expert in consumer finance contracts such as loan agreements, "
        "credit card terms and insurance policies. You help ordinary people understand "
        "what they are signing."
    ),
    "risk_checklist": [
        "Interest rate, compounding method and whether the rate is variable or can change",
        "Late payment penalties and how they are calculated (convert to a yearly % if possible)",
        "Prepayment or foreclosure charges",
        "Processing, hidden, or administrative fees",
        "Clauses letting the lender change terms unilaterally or without notice",
        "Collateral, guarantor or co-signer obligations",
        "Acceleration clauses (lender demands full repayment immediately)",
        "Cross-default clauses and automatic debit permissions",
        "Waiver of the borrower's rights, or forced arbitration",
        "Vague or undefined terms that favour the lender",
    ],
    # Each entry: the term, words that trigger it, and a plain-English meaning
    "glossary": [
        {
            "term": "Principal",
            "aliases": ["principal"],
            "meaning": "The original amount of money you borrow, before any interest is added.",
        },
        {
            "term": "Per annum",
            "aliases": ["per annum", "p.a", "per year"],
            "meaning": "Latin for 'per year'. A rate of 12% per annum means 12% of the amount owed, each year.",
        },
        {
            "term": "Compound interest",
            "aliases": ["compounded", "compounding", "compound interest"],
            "meaning": "Interest charged on your balance plus the interest already added. It grows faster than simple interest because you pay interest on interest.",
        },
        {
            "term": "Simple interest",
            "aliases": ["simple interest"],
            "meaning": "Interest calculated only on the original amount borrowed, never on past interest.",
        },
        {
            "term": "APR (annual percentage rate)",
            "aliases": ["annual percentage rate"],
            "meaning": "The yearly cost of borrowing including fees, not just the interest rate. It is the best number for comparing loans.",
        },
        {
            "term": "EMI (equated monthly instalment)",
            "aliases": ["emi", "equated monthly instalment", "equated monthly installment"],
            "meaning": "A fixed amount you pay every month, made up of part of the principal and part of the interest.",
        },
        {
            "term": "Fixed vs floating rate",
            "aliases": ["floating rate", "variable rate", "fixed rate", "fixed interest"],
            "meaning": "A fixed rate stays the same for the whole loan. A floating (variable) rate can go up or down, so your payments can change.",
        },
        {
            "term": "Late payment penalty",
            "aliases": ["penalty", "penal interest", "late fee", "late payment"],
            "meaning": "An extra charge when you pay after the due date. Check how it is calculated, because a monthly penalty adds up to a much bigger yearly cost.",
        },
        {
            "term": "Default",
            "aliases": ["default", "defaults", "in default"],
            "meaning": "Failing to do what the loan agreement requires, most often missing payments. It usually triggers penalties and can lead to the lender demanding all the money back.",
        },
        {
            "term": "Acceleration clause",
            "aliases": ["acceleration", "accelerate", "immediately due and payable", "become due and payable"],
            "meaning": "A clause letting the lender demand the entire remaining loan at once, usually after you default.",
        },
        {
            "term": "Cross-default",
            "aliases": ["cross-default", "cross default"],
            "meaning": "If you default on any other loan, the lender can treat this loan as defaulted too.",
        },
        {
            "term": "Collateral / security",
            "aliases": ["collateral", "hypothecation", "pledge", "pledged", "mortgage"],
            "meaning": "Something valuable (a house, a car, gold) you promise the lender can take if you do not repay.",
        },
        {
            "term": "Guarantor",
            "aliases": ["guarantor", "guarantee", "guaranteed"],
            "meaning": "A person who promises to repay your loan if you cannot. They are legally responsible for it.",
        },
        {
            "term": "Co-borrower / co-signer",
            "aliases": ["co-borrower", "co-signer", "cosigner", "co-applicant"],
            "meaning": "A second person who shares responsibility for the whole loan, not just half of it.",
        },
        {
            "term": "Prepayment / foreclosure",
            "aliases": ["prepayment", "pre-payment", "foreclosure", "pre-closure", "early repayment", "prepay"],
            "meaning": "Paying off the loan before the end date. Some lenders charge a fee for this, so always check.",
        },
        {
            "term": "Processing fee",
            "aliases": ["processing fee", "administrative fee", "origination fee", "documentation charges"],
            "meaning": "A one-time charge for setting up the loan, often taken from the amount you receive.",
        },
        {
            "term": "Amortization",
            "aliases": ["amortization", "amortisation"],
            "meaning": "The schedule showing how each payment is split between principal and interest over the life of the loan.",
        },
        {
            "term": "Grace period",
            "aliases": ["grace period", "grace days"],
            "meaning": "Extra days after the due date during which you can still pay without a penalty.",
        },
        {
            "term": "Lock-in period",
            "aliases": ["lock-in", "lock in period"],
            "meaning": "A time during which you cannot close or repay the loan early without a charge.",
        },
        {
            "term": "Auto-debit / standing instruction",
            "aliases": ["auto-debit", "auto debit", "automatic debit", "standing instruction", "nach", "ecs mandate"],
            "meaning": "Permission for the lender to take payments directly from your bank account on the due date.",
        },
        {
            "term": "Arbitration",
            "aliases": ["arbitration", "arbitrator"],
            "meaning": "Settling a dispute privately through an arbitrator instead of going to court. Forced arbitration can limit your options.",
        },
        {
            "term": "Waiver",
            "aliases": ["waiver", "waive", "waives"],
            "meaning": "Giving up a right you would normally have. Read carefully, because waivers usually favour the lender.",
        },
        {
            "term": "Indemnity",
            "aliases": ["indemnify", "indemnity", "indemnification"],
            "meaning": "A promise to cover the other party's losses or costs, which can make you responsible for the lender's expenses.",
        },
        {
            "term": "Lien",
            "aliases": ["lien"],
            "meaning": "A legal claim on your property until the debt is paid.",
        },
        {
            "term": "Moratorium",
            "aliases": ["moratorium"],
            "meaning": "A period during which you are allowed to pause repayments. Interest may still be charged.",
        },
        {
            "term": "Balloon payment",
            "aliases": ["balloon payment", "balloon"],
            "meaning": "A very large final payment due at the end, after smaller payments before it.",
        },
    ],
}