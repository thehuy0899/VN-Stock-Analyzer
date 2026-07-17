def calculate_terminal_value(
    last_fcf,
    wacc,
    terminal_growth=0.03,
):
    terminal_value = (
        last_fcf
        * (1 + terminal_growth)
    ) / (
        wacc - terminal_growth
    )

    return {
        "terminal_growth": terminal_growth,
        "terminal_value": terminal_value,
    }