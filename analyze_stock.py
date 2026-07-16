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
    print("GROWTH DRIVER:")

    print(
        final_analysis_result.get(
            "growth_driver"
        )
    )

    print()
    print("GROWTH QUALITY:")

    print(
        final_analysis_result.get(
            "growth_quality"
        )
    )

    print()
    print("CAPITAL QUALITY:")

    print(
        final_analysis_result.get(
            "capital_quality"
        )
    )

    print()
    print("KEY WATCH:")

    print(
        final_analysis_result.get(
            "key_watch"
        )
    )

    print()
    print("FULL THESIS:")

    print(
        final_analysis_result.get(
            "thesis"
        )
    )