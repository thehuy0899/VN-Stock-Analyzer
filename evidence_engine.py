def format_percent(value):
    if value is None:
        return "N/A"

    return f"{value:.2f}%"


def format_point_change(value):
    if value is None:
        return "N/A"

    return f"{value:+.2f} điểm %"


def build_margin_evidence(margin_result):
    if margin_result.get("status") != "success":
        return {
            "status": "error",
            "message": "Không thể tạo bằng chứng cho phân tích biên lợi nhuận.",
        }

    gross_margin = margin_result.get("gross_margin")
    gross_margin_change = margin_result.get(
        "gross_margin_change"
    )

    operating_margin = margin_result.get(
        "operating_margin"
    )
    operating_margin_change = margin_result.get(
        "operating_margin_change"
    )

    selling_ratio_change = margin_result.get(
        "selling_ratio_change"
    )

    admin_ratio_change = margin_result.get(
        "admin_ratio_change"
    )

    gross_margin_first = None

    if (
        gross_margin is not None
        and gross_margin_change is not None
    ):
        gross_margin_first = (
            gross_margin - gross_margin_change
        )

    operating_margin_first = None

    if (
        operating_margin is not None
        and operating_margin_change is not None
    ):
        operating_margin_first = (
            operating_margin
            - operating_margin_change
        )

    evidence = {}

    evidence["gross_margin"] = {
        "first": gross_margin_first,
        "current": gross_margin,
        "change": gross_margin_change,
        "first_text": format_percent(
            gross_margin_first
        ),
        "current_text": format_percent(
            gross_margin
        ),
        "change_text": format_point_change(
            gross_margin_change
        ),
    }

    evidence["operating_margin"] = {
        "first": operating_margin_first,
        "current": operating_margin,
        "change": operating_margin_change,
        "first_text": format_percent(
            operating_margin_first
        ),
        "current_text": format_percent(
            operating_margin
        ),
        "change_text": format_point_change(
            operating_margin_change
        ),
    }

    evidence["selling_ratio"] = {
        "change": selling_ratio_change,
        "change_text": format_point_change(
            selling_ratio_change
        ),
    }

    evidence["admin_ratio"] = {
        "change": admin_ratio_change,
        "change_text": format_point_change(
            admin_ratio_change
        ),
    }

    return {
        "status": "success",
        "evidence": evidence,
    }


def format_number(value):
    if value is None:
        return "N/A"

    return f"{value:,.0f}"
def format_money(value):
    if value is None:
        return "N/A"

    return f"{value:,.0f}"

def format_money_billion(value):
    if value is None:
        return "N/A"

    return f"{value / 1_000_000_000:,.0f} tỷ đồng"


def format_multiple(value):
    if value is None:
        return "N/A"

    return f"{value:.2f} lần"


def build_growth_evidence(growth_result):
    if growth_result.get("status") != "success":
        return {
            "status": "error",
            "message": "Không thể tạo bằng chứng tăng trưởng.",
        }

    first_year = growth_result.get("first_year")
    latest_year = growth_result.get("latest_year")
    history = growth_result.get("history", {})

    first_data = history.get(first_year, {})
    latest_data = history.get(latest_year, {})

    revenue_first = first_data.get("revenue")
    revenue_current = latest_data.get("revenue")

    profit_first = first_data.get("profit")
    profit_current = latest_data.get("profit")

    revenue_growth = growth_result.get("revenue_growth")
    profit_growth = growth_result.get("profit_growth")

    evidence = {
        "revenue": {
            "first_year": first_year,
            "latest_year": latest_year,
            "first": revenue_first,
            "current": revenue_current,
            "growth": revenue_growth,
            "first_text": format_number(
                revenue_first
            ),
            "current_text": format_number(
                revenue_current
            ),
            "growth_text": format_percent(
                revenue_growth
            ),
        },
        "profit": {
            "first_year": first_year,
            "latest_year": latest_year,
            "first": profit_first,
            "current": profit_current,
            "growth": profit_growth,
            "first_text": format_number(
                profit_first
            ),
            "current_text": format_number(
                profit_current
            ),
            "growth_text": format_percent(
                profit_growth
            ),
        },
    }

    if (
        revenue_growth is not None
        and profit_growth is not None
    ):
        difference = (
            profit_growth
            - revenue_growth
        )

        evidence["profit_vs_revenue"] = {
            "difference": difference,
            "difference_text": format_point_change(
                difference
            ),
        }

    return {
        "status": "success",
        "evidence": evidence,
    }


def build_cashflow_evidence(cashflow_result):
    if (
        cashflow_result is None
        or cashflow_result.get("status") != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Không thể tạo bằng chứng "
                "cho phân tích dòng tiền."
            ),
        }

    operating_cashflow = cashflow_result.get(
        "operating_cashflow"
    )

    capex = cashflow_result.get(
        "capex"
    )

    free_cashflow = cashflow_result.get(
        "free_cashflow"
    )

    cash_conversion = cashflow_result.get(
        "cash_conversion"
    )

    evidence = {
        "operating_cashflow": {
            "current": operating_cashflow,
            "current_text": format_money_billion(
                operating_cashflow
            ),
        },
        "capex": {
            "current": capex,
            "current_text": format_money_billion(
                abs(capex)
                if capex is not None
                else None
            ),
        },
        "free_cashflow": {
            "current": free_cashflow,
            "current_text": format_money_billion(
                free_cashflow
            ),
        },
        "cash_conversion": {
            "current": cash_conversion,
            "current_text": format_multiple(
                cash_conversion
            ),
        },
    }

    return {
        "status": "success",
        "evidence": evidence,
    }
def build_balance_sheet_evidence(
    balance_result,
):
    if (
        balance_result is None
        or balance_result.get("status")
        != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Không thể tạo bằng chứng "
                "bảng cân đối kế toán."
            ),
        }

    total_debt = balance_result.get(
        "total_debt"
    )

    net_debt = balance_result.get(
        "net_debt"
    )

    debt_to_equity = balance_result.get(
        "debt_to_equity"
    )

    net_debt_to_equity = balance_result.get(
        "net_debt_to_equity"
    )

    debt_to_assets = balance_result.get(
        "debt_to_assets"
    )

    equity_to_assets = balance_result.get(
        "equity_to_assets"
    )

    debt_change = balance_result.get(
        "debt_change"
    )

    evidence = {
        "total_debt": {
            "current": total_debt,
            "current_text": format_money_billion(
                total_debt
            ),
        },
        "net_debt": {
            "current": net_debt,
            "current_text": format_money_billion(
                net_debt
            ),
        },
        "debt_to_equity": {
            "current": debt_to_equity,
            "current_text": format_multiple(
                debt_to_equity
            ),
        },
        "net_debt_to_equity": {
            "current": net_debt_to_equity,
            "current_text": format_multiple(
                net_debt_to_equity
            ),
        },
        "debt_to_assets": {
            "current": debt_to_assets,
            "current_text": format_percent(
                (
                    debt_to_assets * 100
                    if debt_to_assets is not None
                    else None
                )
            ),
        },
        "equity_to_assets": {
            "current": equity_to_assets,
            "current_text": format_percent(
                (
                    equity_to_assets * 100
                    if equity_to_assets is not None
                    else None
                )
            ),
        },
        "debt_change": {
            "current": debt_change,
            "current_text": format_percent(
                debt_change
            ),
        },
    }

    return {
        "status": "success",
        "evidence": evidence,
    }
def build_capital_efficiency_evidence(
    capital_efficiency_result,
):
    if (
        capital_efficiency_result is None
        or capital_efficiency_result.get("status")
        != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Capital efficiency result "
                "is not available."
            ),
            "evidence": {},
        }

    latest_year = (
        capital_efficiency_result.get(
            "latest_year"
        )
    )

    latest_roic = (
        capital_efficiency_result.get(
            "latest_roic"
        )
    )

    previous_roic = (
        capital_efficiency_result.get(
            "previous_roic"
        )
    )

    roic_change = (
        capital_efficiency_result.get(
            "roic_change"
        )
    )

    roic_class = (
        capital_efficiency_result.get(
            "roic_class"
        )
    )

    incremental_roic = (
        capital_efficiency_result.get(
            "incremental_roic"
        )
    )

    incremental_roic_class = (
        capital_efficiency_result.get(
            "incremental_roic_class"
        )
    )

    capital_efficiency_regime = (
        capital_efficiency_result.get(
            "capital_efficiency_regime"
        )
    )

    signals = (
        capital_efficiency_result.get(
            "signals",
            [],
        )
    )

    capital_history = (
        capital_efficiency_result.get(
            "capital_history",
            [],
        )
    )

    diagnostics = (
        capital_efficiency_result.get(
            "diagnostics",
            {},
        )
    )

    evidence = {
        "latest_year": latest_year,
        "latest_roic": latest_roic,
        "previous_roic": previous_roic,
        "roic_change": roic_change,
        "roic_class": roic_class,
        "incremental_roic": incremental_roic,
        "incremental_roic_class": (
            incremental_roic_class
        ),
        "capital_efficiency_regime": (
            capital_efficiency_regime
        ),
        "signals": signals,
        "capital_history": capital_history,
        "diagnostics": diagnostics,
    }

    return {
        "status": "success",
        "evidence": evidence,
    }