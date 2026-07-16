from evidence_engine import (
    build_margin_evidence,
    build_growth_evidence,
    build_cashflow_evidence,
    build_balance_sheet_evidence,
)

from narrative_engine import build_narratives
from conclusion_engine import build_conclusion


def generate_final_analysis(
    margin_result,
    growth_result,
    cross_result,
    health_result,
    cashflow_result=None,
    balance_result=None,
    financial_cross_result=None,
    growth_quality_result=None,
    earnings_driver_result=None,
    capital_efficiency_result=None,
    capital_allocation_result=None,
):
    strengths = health_result.get(
        "strengths",
        [],
    )

    warnings = health_result.get(
        "warnings",
        [],
    )

    # ==============================
    # BUILD EVIDENCE
    # ==============================

    margin_evidence = {}
    growth_evidence = {}
    cashflow_evidence = {}
    balance_evidence = {}

    # ==============================
    # MARGIN EVIDENCE
    # ==============================

    margin_evidence_result = (
        build_margin_evidence(
            margin_result
        )
    )

    if (
        margin_evidence_result.get(
            "status"
        )
        == "success"
    ):
        margin_evidence = (
            margin_evidence_result.get(
                "evidence",
                {},
            )
        )

    # ==============================
    # GROWTH EVIDENCE
    # ==============================

    growth_evidence_result = (
        build_growth_evidence(
            growth_result
        )
    )

    if (
        growth_evidence_result.get(
            "status"
        )
        == "success"
    ):
        growth_evidence = (
            growth_evidence_result.get(
                "evidence",
                {},
            )
        )

    # ==============================
    # CASHFLOW EVIDENCE
    # ==============================

    if cashflow_result is not None:
        cashflow_evidence_result = (
            build_cashflow_evidence(
                cashflow_result
            )
        )

        if (
            cashflow_evidence_result.get(
                "status"
            )
            == "success"
        ):
            cashflow_evidence = (
                cashflow_evidence_result.get(
                    "evidence",
                    {},
                )
            )

    # ==============================
    # BALANCE SHEET EVIDENCE
    # ==============================

    if balance_result is not None:
        balance_evidence_result = (
            build_balance_sheet_evidence(
                balance_result
            )
        )

        if (
            balance_evidence_result.get(
                "status"
            )
            == "success"
        ):
            balance_evidence = (
                balance_evidence_result.get(
                    "evidence",
                    {},
                )
            )

    # ==============================
    # FINANCIAL CROSS SIGNALS
    # ==============================

    financial_cross_signals = []

    if (
        financial_cross_result is not None
        and financial_cross_result.get(
            "status"
        )
        == "success"
    ):
        financial_cross_signals = (
            financial_cross_result.get(
                "signals",
                [],
            )
        )

    # ==============================
    # GROWTH QUALITY EVIDENCE
    # ==============================

    growth_quality_evidence = {}

    if (
        growth_quality_result is not None
        and growth_quality_result.get(
            "status"
        )
        == "success"
    ):
        growth_quality_evidence = {
            "growth_quality": (
                growth_quality_result.get(
                    "growth_quality"
                )
            ),
            "signals": (
                growth_quality_result.get(
                    "signals",
                    [],
                )
            ),
            "diagnostics": (
                growth_quality_result.get(
                    "diagnostics",
                    {},
                )
            ),
            "profit_history": (
                growth_quality_result.get(
                    "profit_history",
                    [],
                )
            ),
        }

    # ==============================
    # NARRATIVE
    # ==============================

    analysis = build_narratives(
        strengths,
        warnings,
        margin_evidence,
        growth_evidence,
        cashflow_evidence,
        balance_evidence,
        growth_quality_evidence,
        capital_efficiency_result,
    )

    # ==============================
    # CROSS SIGNALS
    # ==============================

    cross_signals = []

    if (
        cross_result is not None
        and cross_result.get(
            "status"
        )
        == "success"
    ):
        cross_signals = (
            cross_result.get(
                "signals",
                [],
            )
        )

    # ==============================
    # CONCLUSION
    # ==============================

    conclusion = build_conclusion(
        strengths,
        warnings,
        cross_signals,
        growth_quality_evidence,
    )


    # ==============================
    # RETURN
    # ==============================

    return {
        "status": "success",
        "score": health_result.get(
            "score"
        ),
        "health_class": health_result.get(
            "health_class"
        ),
        "analysis": analysis,
        "conclusion": conclusion,
    }