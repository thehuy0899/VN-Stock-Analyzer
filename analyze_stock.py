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

    