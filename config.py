# config.py

TOPICS = {
    "Tax Deductions": "💼",
    "Policy Query": "📜",
    "Audit & Risk Advisory": "🪙",
    "SME Compliance": "🏢",
    "Corporate Tax Planning": "🏦",
}

PRE_SAVED_ANSWERS = {
    "Tax Deductions": {
        "is home office equipment deductible ?": {
            "response": "Yes, home office equipment is generally deductible under Section 3.2 of the ATO Home Office Expense Deduction. This includes items like desks, chairs, and monitors used primarily for work-from-home purposes.",
            "source": "ATO_guide_2022",
            "section": "Section 3.2",
            "confidence": 0.92
        },
        "can i claim vehicle expenses ?": {
            "response": "Yes, vehicle expenses are deductible if they are directly related to income-generating activities. See Section 4.1 in deductible_items_list.md.",
            "source": "deductible_items_list.md",
            "section": "Section 4.1"
        }
    },
    "Crypto Tax": {
        "is crypto staking taxable ?": {
            "response": "Yes, income earned from staking crypto is considered taxable according to ATO_crypto_policy.pdf, Section 5.1.",
            "source": "ATO_crypto_policy.pdf",
            "section": "Section 5.1"
        },
        "what are capital gains on crypto ?": {
            "response": "Capital gains apply when you dispose of crypto assets. Refer to Section 6.3 in crypto_gain_summary_2023.pdf.",
            "source": "crypto_gain_summary_2023.pdf",
            "section": "Section 6.3"
        }
    },
    "Policy Query": {
    "what are my ongoing tax obligations as a small business": {
        "response": (
            "Small businesses in Australia are required to lodge a Business Activity Statement (BAS) either monthly or quarterly, "
            "report and pay GST, PAYG withholding, and income tax. Employers must also meet superannuation obligations for staff. "
            "These requirements are detailed in Section 3.1 of the ATO_sme_compliance_guide.pdf."
        ),
        "source": "ATO_sme_compliance_guide.pdf",
        "section": "Section 3.1",
        "confidence": 0.85
    }
}

}
