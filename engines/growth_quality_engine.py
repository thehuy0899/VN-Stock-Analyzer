def analyze_growth_quality(
    growth_result,
    margin_result,
):
    if (
        growth_result is None
        or growth_result.get("status")
        != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Không thể phân tích "
                "chất lượng tăng trưởng."
            ),
        }

    if (
        margin_result is None
        or margin_result.get("status")
        != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Không thể phân tích "
                "chất lượng tăng trưởng."
            ),
        }

    signals = []

    revenue_growth = growth_result.get(
        "revenue_growth"
    )

    profit_growth = growth_result.get(
        "profit_growth"
    )

    revenue_cagr = growth_result.get(
        "revenue_cagr"
    )

    profit_cagr = growth_result.get(
        "profit_cagr"
    )

    history = growth_result.get(
        "history",
        {},
    )

    gross_margin_change = margin_result.get(
        "gross_margin_change"
    )

    operating_margin_change = (
        margin_result.get(
            "operating_margin_change"
        )
    )

    # ==============================
    # BUILD PROFIT HISTORY
    # ==============================

    profit_history = []

    for year, data in history.items():
        if not isinstance(data, dict):
            continue

        profit = data.get("profit")

        if profit is None:
            continue

        try:
            year_value = int(year)
            profit_value = float(profit)

        except (
            TypeError,
            ValueError,
        ):
            continue

        profit_history.append(
            {
                "year": year_value,
                "profit": profit_value,
            }
        )

    profit_history.sort(
        key=lambda item: item["year"]
    )

    # ==============================
    # BASIC GROWTH SIGNALS
    # ==============================

    if (
        revenue_growth is not None
        and profit_growth is not None
        and profit_growth > revenue_growth
    ):
        signals.append(
            "profit_growth_faster_than_revenue"
        )

    if (
        revenue_growth is not None
        and revenue_growth >= 10
        and profit_growth is not None
        and profit_growth > 0
    ):
        signals.append(
            "revenue_driven_growth"
        )

    if (
        profit_growth is not None
        and profit_growth >= 20
        and operating_margin_change is not None
        and operating_margin_change > 0
    ):
        signals.append(
            "margin_driven_profit_growth"
        )

    # ==============================
    # HISTORICAL PROFIT ANALYSIS
    # ==============================

    latest_profit = None
    previous_profit = None

    trough_year = None
    trough_profit = None

    pre_trough_peak = None
    pre_trough_average = None

    recovery_from_trough = False
    recovery_above_pre_trough = False

    if len(profit_history) >= 2:
        latest_profit = profit_history[-1][
            "profit"
        ]

        previous_profit = profit_history[-2][
            "profit"
        ]

    # ==============================
    # IDENTIFY HISTORICAL TROUGH
    # ==============================

    if len(profit_history) >= 3:
        historical_period = (
            profit_history[:-1]
        )

        positive_history = [
            item
            for item in historical_period
            if item["profit"] > 0
        ]

        if positive_history:
            trough_item = min(
                positive_history,
                key=lambda item: item["profit"],
            )

            trough_year = trough_item["year"]
            trough_profit = trough_item["profit"]

            pre_trough_history = [
                item["profit"]
                for item in profit_history
                if (
                    item["year"] < trough_year
                    and item["profit"] > 0
                )
            ]

            if pre_trough_history:
                pre_trough_peak = max(
                    pre_trough_history
                )

                pre_trough_average = (
                    sum(pre_trough_history)
                    / len(pre_trough_history)
                )

    # ==============================
    # STRUCTURAL GROWTH
    # ==============================

    if (
        revenue_cagr is not None
        and profit_cagr is not None
        and revenue_cagr >= 10
        and profit_cagr >= 10
    ):
        signals.append(
            "structural_growth"
        )

    # ==============================
    # PROFIT GROWTH QUALITY
    # ==============================

    if (
        revenue_growth is not None
        and profit_growth is not None
        and profit_growth >= 20
        and profit_growth > revenue_growth
    ):
        signals.append(
            "strong_profit_growth_quality"
        )

    # ==============================
    # PROFIT RECOVERY FROM TROUGH
    # ==============================

    if (
        trough_profit is not None
        and pre_trough_peak is not None
        and pre_trough_peak > 0
        and latest_profit is not None
    ):
        trough_ratio = (
            trough_profit
            / pre_trough_peak
        )

        if (
            trough_ratio < 0.75
            and latest_profit > trough_profit
        ):
            signals.append(
                "profit_recovery_from_trough"
            )

            recovery_from_trough = True

    # ==============================
    # RECOVERY VS PRE-TROUGH LEVEL
    # ==============================

    if (
        recovery_from_trough
        and latest_profit is not None
        and pre_trough_peak is not None
        and pre_trough_peak > 0
    ):
        recovery_ratio = (
            latest_profit
            / pre_trough_peak
        )

        if recovery_ratio >= 1.15:
            signals.append(
                "profit_recovery_above_pre_trough_level"
            )

            recovery_above_pre_trough = True

        elif recovery_ratio >= 0.85:
            signals.append(
                "profit_recovery_toward_pre_trough_level"
            )

        else:
            signals.append(
                "early_stage_profit_recovery"
            )

    # ==============================
    # HEURISTIC LOW-BASE WARNING
    # ==============================

    possible_low_base_effect = False

    if (
        not recovery_from_trough
        and profit_growth is not None
        and profit_growth >= 50
        and previous_profit is not None
        and latest_profit is not None
        and latest_profit > previous_profit
    ):
        possible_low_base_effect = True

        signals.append(
            "possible_low_base_effect"
        )

    # ==============================
    # GROSS MARGIN PRESSURE
    # ==============================

    if (
        profit_growth is not None
        and profit_growth > 0
        and gross_margin_change is not None
        and gross_margin_change < 0
    ):
        signals.append(
            "profit_growth_despite_gross_margin_pressure"
        )

    # ==============================
    # FINAL GROWTH QUALITY
    # ==============================

    growth_quality = "mixed"

    if (
        recovery_from_trough
        and recovery_above_pre_trough
    ):
        growth_quality = "recovery_breakout"

    elif recovery_from_trough:
        if (
            "margin_driven_profit_growth"
            in signals
        ):
            growth_quality = (
                "recovery_with_margin_improvement"
            )

        else:
            growth_quality = "recovery"

    elif "structural_growth" in signals:
        growth_quality = "structural"

    elif (
        "margin_driven_profit_growth"
        in signals
    ):
        growth_quality = "margin_driven"

    elif (
        "revenue_driven_growth"
        in signals
    ):
        growth_quality = "revenue_driven"

    elif possible_low_base_effect:
        growth_quality = "possible_low_base"

    # ==============================
    # REMOVE DUPLICATE SIGNALS
    # ==============================

    signals = list(
        dict.fromkeys(signals)
    )

    # ==============================
    # RETURN RESULT
    # ==============================

    return {
        "status": "success",
        "growth_quality": growth_quality,
        "signals": signals,
        "profit_history": profit_history,
        "diagnostics": {
            "latest_profit": latest_profit,
            "previous_profit": previous_profit,
            "trough_year": trough_year,
            "trough_profit": trough_profit,
            "pre_trough_peak": pre_trough_peak,
            "pre_trough_average": (
                pre_trough_average
            ),
            "recovery_from_trough": (
                recovery_from_trough
            ),
            "recovery_above_pre_trough": (
                recovery_above_pre_trough
            ),
        },
        "message": None,
    }