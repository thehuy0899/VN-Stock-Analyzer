from analysis_pipeline import (
    run_analysis_for_symbol,
)


def analyze_stock(
    symbol,
):
    symbol = symbol.upper().strip()

    result = run_analysis_for_symbol(
        symbol
    )

    return result


if __name__ == "__main__":
    symbol = input(
        "Nhap ma co phieu: "
    )

    result = analyze_stock(
        symbol
    )

    health_result = result[
        "health"
    ]

    final_analysis_result = result[
        "final_analysis"
    ]

    print()
    print("=" * 60)
    print(
        "SYMBOL:",
        symbol.upper().strip(),
    )

    print(
        "STATUS:",
        final_analysis_result.get(
            "status"
        ),
    )

    print(
        "SCORE:",
        final_analysis_result.get(
            "score"
        ),
    )

    print(
        "HEALTH CLASS:",
        final_analysis_result.get(
            "health_class"
        ),
    )

    print()
    print("PIOTROSKI:")
    print(
        "Score:",
        result["piotroski"]["score"],
    )
    print(
        "Level:",
        result["piotroski"]["level"],
    )

    print()
    print("ALTMAN Z SCORE:")
    print(
        "Score:",
        result["altman"]["score"],
    )
    print(
        "Level:",
        result["altman"]["level"],
    )


    print()
    print("BENEISH M-SCORE:")
    print(
        "Score:",
        result["beneish"]["score"],
    )
    print(
        "Level:",
        result["beneish"]["level"],
    )

    print()
    print("DCF:")

    if result["dcf"]["status"] == "success":

        print(
            "WACC:",
            f"{result['dcf']['wacc']['wacc']:.2%}",
        )
        print(
            "FCF:",
            f"{result['dcf']['fcf']:,.0f}",
        )

        print(
            "Projection:",
        )

        for i, value in enumerate(
            result["dcf"]["projection"],
            start=1,
        ):
            print(
                f"Year {i}: {value:,.0f}"
            )

        print("\nPresent Value:")

        for i, value in enumerate(
            result["dcf"]["present_values"],
            start=1,
        ):
            print(
                f"Year {i}: {value:,.0f}"
            )

        print()
        print(
            "Terminal Value:",
            f"{result['dcf']['terminal']['terminal_value']:,.0f}",
        )

        print(
            "Enterprise Value:",
            f"{result['dcf']['enterprise_value']:,.0f}",
        )

        print(
            "Net Debt:",
            f"{result['dcf']['net_debt']:,.0f}",
        )

        print(
            "Equity Value:",
            f"{result['dcf']['equity_value']:,.0f}",
        )

        print(
            "Intrinsic Value / Share:",
            f"{result['dcf']['intrinsic_value']:,.2f}",
        )

        print(
            "Current Price:",
            f"{result['dcf']['current_price']:,.2f}",
        )

        print(
            "Margin of Safety:",
            f"{result['dcf']['margin_of_safety']:.2f}%",
        )

    else:
        print(
            result["dcf"]["message"]
        )

    print()
    print("STRENGTHS:")

    for signal in health_result.get(
        "strengths",
        [],
    ):
        print(
            "-",
            signal,
        )

    print()
    print("WARNINGS:")

    for signal in health_result.get(
        "warnings",
        [],
    ):
        print(
            "-",
            signal,
        )

    print()
    print("\nANALYSIS:")

    for item in final_analysis_result["analysis"]:
        print(f"- {item}")

    print("\nCONCLUSION:")
    print(final_analysis_result["conclusion"])

    print()
    print("RELATIVE VALUATION")

    relative = result["relative_valuation"]

    print("PE:", relative["pe"])
    print("PB:", relative["pb"])
    print("EV/EBITDA:", relative["ev_ebitda"])

    if relative["valuation"]:
        print("Signals:")
        for signal in relative["valuation"]:
            print("-", signal)
    else:
        print("No valuation signal.")
    