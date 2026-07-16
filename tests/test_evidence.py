from data_loader import load_income_statement
from analysis_engine import analyze_margin
from evidence_engine import build_margin_evidence


symbol = "FPT"

income = load_income_statement(
    symbol
)

margin_result = analyze_margin(
    income
)

evidence_result = build_margin_evidence(
    margin_result
)

print(
    "\nTEST EVIDENCE ENGINE"
)

print(
    "=" * 60
)

print(
    "Trang thai:",
    evidence_result["status"]
)

if evidence_result["status"] == "success":
    evidence = evidence_result["evidence"]

    print(
        "Gross Margin:",
        evidence["gross_margin"]
    )

    print(
        "Operating Margin:",
        evidence["operating_margin"]
    )

    print(
        "Selling Ratio:",
        evidence["selling_ratio"]
    )

    print(
        "Admin Ratio:",
        evidence["admin_ratio"]
    )
else:
    print(
        evidence_result["message"]
    )