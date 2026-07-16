def analyze_earnings_drivers(
    growth_result,
    margin_result,
    growth_quality_result=None,
):
    if (
        growth_result is None
        or margin_result is None
    ):
        return {
            "status": "error",
            "message": (
                "Missing growth or margin result"
            ),
        }

    if (
        growth_result.get("status")
        != "success"
        or margin_result.get("status")
        != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Growth or margin analysis "
                "is not successful"
            ),
        }

    # ==============================
    # INPUT DATA
    # ==============================

    revenue_growth = (
        growth_result.get(
            "revenue_growth"
        )
        or 0
    )

    profit_growth = (
        growth_result.get(
            "profit_growth"
        )
        or 0
    )

    gross_margin_change = (
        margin_result.get(
            "gross_margin_change"
        )
        or 0
    )

    operating_margin_change = (
        margin_result.get(
            "operating_margin_change"
        )
        or 0
    )

    selling_ratio_change = (
        margin_result.get(
            "selling_ratio_change"
        )
        or 0
    )

    admin_ratio_change = (
        margin_result.get(
            "admin_ratio_change"
        )
        or 0
    )

    growth_quality = None

    if growth_quality_result is not None:
        growth_quality = (
            growth_quality_result.get(
                "growth_quality"
            )
        )

    # ==============================
    # GROWTH REGIME
    # ==============================

    growth_regime = growth_quality

    # ==============================
    # FUNDAMENTAL DRIVER SCORES
    # ==============================

    driver_scores = {
        "revenue_expansion": 0,
        "gross_margin_expansion": 0,
        "selling_efficiency": 0,
        "admin_efficiency": 0,
    }

    # ==============================
    # OFFSET SCORES
    # ==============================

    offset_scores = {
        "revenue_pressure": 0,
        "gross_margin_pressure": 0,
        "selling_cost_pressure": 0,
        "admin_cost_pressure": 0,
    }

    # ==============================
    # REVENUE DRIVER
    # ==============================

    if revenue_growth >= 15:
        driver_scores[
            "revenue_expansion"
        ] = 3

    elif revenue_growth >= 8:
        driver_scores[
            "revenue_expansion"
        ] = 2

    elif revenue_growth >= 3:
        driver_scores[
            "revenue_expansion"
        ] = 1

    elif revenue_growth < 0:
        offset_scores[
            "revenue_pressure"
        ] = 2

    # ==============================
    # GROSS MARGIN DRIVER
    # ==============================

    if gross_margin_change >= 2:
        driver_scores[
            "gross_margin_expansion"
        ] = 3

    elif gross_margin_change >= 0.5:
        driver_scores[
            "gross_margin_expansion"
        ] = 2

    elif gross_margin_change <= -2:
        offset_scores[
            "gross_margin_pressure"
        ] = 3

    elif gross_margin_change <= -0.5:
        offset_scores[
            "gross_margin_pressure"
        ] = 2

    # ==============================
    # SELLING EFFICIENCY
    # ==============================

    if selling_ratio_change <= -3:
        driver_scores[
            "selling_efficiency"
        ] = 3

    elif selling_ratio_change <= -1:
        driver_scores[
            "selling_efficiency"
        ] = 2

    elif selling_ratio_change <= -0.3:
        driver_scores[
            "selling_efficiency"
        ] = 1

    elif selling_ratio_change >= 2:
        offset_scores[
            "selling_cost_pressure"
        ] = 2

    elif selling_ratio_change >= 0.5:
        offset_scores[
            "selling_cost_pressure"
        ] = 1

    # ==============================
    # ADMIN EFFICIENCY
    # ==============================

    if admin_ratio_change <= -2:
        driver_scores[
            "admin_efficiency"
        ] = 3

    elif admin_ratio_change <= -1:
        driver_scores[
            "admin_efficiency"
        ] = 2

    elif admin_ratio_change <= -0.3:
        driver_scores[
            "admin_efficiency"
        ] = 1

    elif admin_ratio_change >= 2:
        offset_scores[
            "admin_cost_pressure"
        ] = 2

    elif admin_ratio_change >= 0.5:
        offset_scores[
            "admin_cost_pressure"
        ] = 1

    # ==============================
    # RANK FUNDAMENTAL DRIVERS
    # ==============================

    ranked_drivers = sorted(
        [
            {
                "driver": driver,
                "score": score,
            }
            for driver, score
            in driver_scores.items()
            if score > 0
        ],
        key=lambda item: item["score"],
        reverse=True,
    )

    ranked_offsets = sorted(
        [
            {
                "factor": factor,
                "score": score,
            }
            for factor, score
            in offset_scores.items()
            if score > 0
        ],
        key=lambda item: item["score"],
        reverse=True,
    )

    # ==============================
    # PRIMARY DRIVER GROUP
    # ==============================

    primary_drivers = []
    secondary_drivers = []

    if ranked_drivers:
        highest_score = ranked_drivers[0][
            "score"
        ]

        primary_drivers = [
            item["driver"]
            for item in ranked_drivers
            if item["score"] == highest_score
        ]

        secondary_drivers = [
            item["driver"]
            for item in ranked_drivers
            if item["score"] < highest_score
        ]

    # ==============================
    # EARNINGS MECHANISM
    # ==============================

    earnings_mechanism = []

    growth_gap = (
        profit_growth - revenue_growth
    )

    if (
        profit_growth > revenue_growth
        and operating_margin_change > 0
    ):
        earnings_mechanism.append(
            "operating_leverage"
        )

    if (
        driver_scores[
            "selling_efficiency"
        ] > 0
        and operating_margin_change > 0
    ):
        earnings_mechanism.append(
            "cost_efficiency_transmission"
        )

    if (
        gross_margin_change < 0
        and operating_margin_change > 0
    ):
        earnings_mechanism.append(
            "operating_efficiency_offset"
        )

    # ==============================
    # OFFSET FACTORS
    # ==============================

    offset_factors = [
        item["factor"]
        for item in ranked_offsets
    ]

    # ==============================
    # DRIVER PROFILE
    # ==============================

    if (
        "revenue_expansion"
        in primary_drivers
        and "selling_efficiency"
        in primary_drivers
    ):
        driver_profile = (
            "revenue_and_efficiency_driven"
        )

    elif (
        "revenue_expansion"
        in primary_drivers
    ):
        driver_profile = "revenue_driven"

    elif (
        "gross_margin_expansion"
        in primary_drivers
    ):
        driver_profile = "margin_driven"

    elif (
        "selling_efficiency"
        in primary_drivers
        or "admin_efficiency"
        in primary_drivers
    ):
        driver_profile = "cost_efficiency_driven"

    else:
        driver_profile = "unclear"

    # ==============================
    # SIGNALS
    # ==============================

    signals = []

    if primary_drivers:
        signals.append(
            "earnings_drivers_identified"
        )

    if (
        driver_scores[
            "revenue_expansion"
        ] > 0
    ):
        signals.append(
            "revenue_supports_profit_growth"
        )

    if (
        driver_scores[
            "gross_margin_expansion"
        ] > 0
    ):
        signals.append(
            "gross_margin_supports_earnings"
        )

    if (
        driver_scores[
            "selling_efficiency"
        ] > 0
    ):
        signals.append(
            "selling_efficiency_supports_earnings"
        )

    if (
        driver_scores[
            "admin_efficiency"
        ] > 0
    ):
        signals.append(
            "admin_efficiency_supports_earnings"
        )

    if (
        "operating_leverage"
        in earnings_mechanism
    ):
        signals.append(
            "operating_leverage_transmits_growth"
        )

    if (
        "operating_efficiency_offset"
        in earnings_mechanism
    ):
        signals.append(
            "operating_efficiency_offsets_gross_pressure"
        )

    if (
        offset_scores[
            "gross_margin_pressure"
        ] > 0
    ):
        signals.append(
            "gross_margin_offsets_earnings_growth"
        )

    # ==============================
    # DIAGNOSTICS
    # ==============================

    diagnostics = {
        "revenue_growth": revenue_growth,
        "profit_growth": profit_growth,
        "growth_gap": growth_gap,
        "gross_margin_change": (
            gross_margin_change
        ),
        "operating_margin_change": (
            operating_margin_change
        ),
        "selling_ratio_change": (
            selling_ratio_change
        ),
        "admin_ratio_change": (
            admin_ratio_change
        ),
    }

    # ==============================
    # RETURN
    # ==============================

    return {
        "status": "success",
        "growth_regime": growth_regime,
        "driver_profile": driver_profile,
        "primary_drivers": primary_drivers,
        "secondary_drivers": (
            secondary_drivers
        ),
        "earnings_mechanism": (
            earnings_mechanism
        ),
        "offset_factors": offset_factors,
        "driver_scores": driver_scores,
        "offset_scores": offset_scores,
        "ranked_drivers": ranked_drivers,
        "ranked_offsets": ranked_offsets,
        "signals": signals,
        "diagnostics": diagnostics,
    }