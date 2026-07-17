def calculate_wacc(
    cost_of_equity=0.15,
    cost_of_debt=0.08,
    equity_weight=0.7,
    debt_weight=0.3,
    tax_rate=0.20,
):
    wacc = (
        equity_weight * cost_of_equity
        + debt_weight * cost_of_debt * (1 - tax_rate)
    )

    return {
        "cost_of_equity": cost_of_equity,
        "cost_of_debt": cost_of_debt,
        "tax_rate": tax_rate,
        "equity_weight": equity_weight,
        "debt_weight": debt_weight,
        "wacc": round(wacc, 4),
    }