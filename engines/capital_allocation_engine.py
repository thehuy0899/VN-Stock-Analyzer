def analyze_capital_allocation(
    capital_efficiency_result,
):
    # ==============================
    # VALIDATE INPUT
    # ==============================

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
        }

    # ==============================
    # EXTRACT CAPITAL DATA
    # ==============================

    capital_history = (
        capital_efficiency_result.get(
            "history",
            [],
        )
        or []
    )

    latest_roic = (
        capital_efficiency_result.get(
            "latest_roic"
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

    if len(capital_history) < 2:
        return {
            "status": "error",
            "message": (
                "Insufficient capital history."
            ),
            "diagnostics": {
                "history_length": len(
                    capital_history
                ),
                "available_keys": list(
                    capital_efficiency_result.keys()
                ),
            },
        }

    # ==============================
    # SORT HISTORY
    # ==============================

    history = sorted(
        capital_history,
        key=lambda item: item.get(
            "year",
            0,
        ),
    )

    previous = history[-2]
    latest = history[-1]

    # ==============================
    # EXTRACT LATEST PERIOD DATA
    # ==============================

    previous_invested_capital = (
        previous.get(
            "invested_capital"
        )
    )

    latest_invested_capital = (
        latest.get(
            "invested_capital"
        )
    )

    previous_nopat = (
        previous.get(
            "nopat"
        )
    )

    latest_nopat = (
        latest.get(
            "nopat"
        )
    )

    # ==============================
    # VALIDATE REQUIRED VALUES
    # ==============================

    required_values = {
        "previous_invested_capital": (
            previous_invested_capital
        ),
        "latest_invested_capital": (
            latest_invested_capital
        ),
        "previous_nopat": (
            previous_nopat
        ),
        "latest_nopat": (
            latest_nopat
        ),
    }

    missing_items = [
        key
        for key, value
        in required_values.items()
        if value is None
    ]

    if missing_items:
        return {
            "status": "error",
            "message": (
                "Required capital allocation "
                "items were not found."
            ),
            "missing_items": missing_items,
            "diagnostics": {
                "previous_period": previous,
                "latest_period": latest,
            },
        }

    # ==============================
    # CAPITAL CHANGE
    # ==============================

    invested_capital_change = (
        latest_invested_capital
        - previous_invested_capital
    )

    if previous_invested_capital != 0:
        invested_capital_growth = (
            invested_capital_change
            / abs(
                previous_invested_capital
            )
        )
    else:
        invested_capital_growth = None

    # ==============================
    # NOPAT CHANGE
    # ==============================

    nopat_change = (
        latest_nopat
        - previous_nopat
    )

    if previous_nopat != 0:
        nopat_growth = (
            nopat_change
            / abs(previous_nopat)
        )
    else:
        nopat_growth = None

    # ==============================
    # REINVESTMENT INTENSITY
    # ==============================

    if invested_capital_growth is None:
        reinvestment_intensity = None

    elif invested_capital_growth >= 0.20:
        reinvestment_intensity = "high"

    elif invested_capital_growth >= 0.10:
        reinvestment_intensity = "moderate"

    elif invested_capital_growth > 0:
        reinvestment_intensity = "low"

    else:
        reinvestment_intensity = (
            "capital_contraction"
        )

    # ==============================
    # CAPITAL ALLOCATION REGIME
    # ==============================

    allocation_regime = None

    if (
        invested_capital_growth is not None
        and invested_capital_growth >= 0.10
        and incremental_roic_class
        in {
            "excellent",
            "strong",
        }
    ):
        allocation_regime = (
            "productive_reinvestment"
        )

    elif (
        invested_capital_growth is not None
        and invested_capital_growth >= 0.10
        and incremental_roic_class
        in {
            "weak",
            "poor",
        }
    ):
        allocation_regime = (
            "capital_intensive_low_return_growth"
        )

    elif (
        invested_capital_growth is not None
        and invested_capital_growth < 0.10
        and latest_roic is not None
        and latest_roic >= 0.15
    ):
        allocation_regime = (
            "mature_high_return_business"
        )

    elif (
        invested_capital_growth is not None
        and invested_capital_growth <= 0
    ):
        allocation_regime = (
            "capital_contraction"
        )

    else:
        allocation_regime = (
            "balanced_reinvestment"
        )

    # ==============================
    # SIGNALS
    # ==============================

    signals = []

    if (
        invested_capital_growth is not None
        and invested_capital_growth >= 0.10
    ):
        signals.append(
            "meaningful_capital_reinvestment"
        )

    if (
        invested_capital_growth is not None
        and invested_capital_growth >= 0.20
    ):
        signals.append(
            "high_reinvestment_intensity"
        )

    if incremental_roic_class == "excellent":
        signals.append(
            "excellent_incremental_returns"
        )

    elif incremental_roic_class == "strong":
        signals.append(
            "strong_incremental_returns"
        )

    elif incremental_roic_class in {
        "weak",
        "poor",
    }:
        signals.append(
            "weak_incremental_returns"
        )

    if (
        incremental_roic is not None
        and latest_roic is not None
        and incremental_roic > latest_roic
    ):
        signals.append(
            "new_capital_more_productive"
        )

    if (
        nopat_growth is not None
        and invested_capital_growth is not None
        and nopat_growth
        > invested_capital_growth
    ):
        signals.append(
            "profit_growth_outpaces_capital_growth"
        )

    if (
        allocation_regime
        == "productive_reinvestment"
    ):
        signals.append(
            "productive_capital_allocation"
        )

    elif (
        allocation_regime
        == "capital_intensive_low_return_growth"
    ):
        signals.append(
            "capital_allocation_efficiency_risk"
        )

    # ==============================
    # RETURN
    # ==============================

    return {
        "status": "success",
        "latest_year": latest.get(
            "year"
        ),
        "previous_year": previous.get(
            "year"
        ),
        "allocation_regime": (
            allocation_regime
        ),
        "reinvestment_intensity": (
            reinvestment_intensity
        ),
        "invested_capital_change": (
            invested_capital_change
        ),
        "invested_capital_growth": (
            invested_capital_growth
        ),
        "nopat_change": (
            nopat_change
        ),
        "nopat_growth": (
            nopat_growth
        ),
        "latest_roic": (
            latest_roic
        ),
        "incremental_roic": (
            incremental_roic
        ),
        "incremental_roic_class": (
            incremental_roic_class
        ),
        "capital_efficiency_regime": (
            capital_efficiency_regime
        ),
        "signals": signals,
        "diagnostics": {
            "history_length": len(
                history
            ),
            "previous_invested_capital": (
                previous_invested_capital
            ),
            "latest_invested_capital": (
                latest_invested_capital
            ),
            "previous_nopat": (
                previous_nopat
            ),
            "latest_nopat": (
                latest_nopat
            ),
        },
    }