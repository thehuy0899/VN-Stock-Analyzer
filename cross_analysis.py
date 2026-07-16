def analyze_cross_signals(
    margin_result,
    growth_result,
):
    signals = []

    margin_signals = set(
        margin_result.get(
            "signals",
            []
        )
    )

    growth_signals = set(
        growth_result.get(
            "signals",
            []
        )
    )

    if (
        "profit_growth_faster_than_revenue"
        in growth_signals
        and
        "operating_margin_up"
        in margin_signals
    ):
        signals.append(
            "operating_leverage_positive"
        )

    if (
        "gross_margin_down"
        in margin_signals
        and
        "operating_margin_up"
        in margin_signals
    ):
        signals.append(
            "cost_efficiency_offset_gross_pressure"
        )

    if (
        "admin_efficiency_improved"
        in margin_signals
        and
        "profit_growth_faster_than_revenue"
        in growth_signals
    ):
        signals.append(
            "admin_efficiency_supports_profit_growth"
        )

    if (
        "strong_revenue_cagr"
        in growth_signals
        and
        "strong_profit_cagr"
        in growth_signals
    ):
        signals.append(
            "strong_long_term_growth"
        )

    return {
        "status": "success",
        "signals": signals,
    }