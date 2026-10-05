CONFIG = {
    "id": "finance",
    "name": "Finance",
    "description": "Loan agreements, credit card terms, insurance policies",
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
}