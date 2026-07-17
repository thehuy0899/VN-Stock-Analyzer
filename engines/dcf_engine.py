from core.dcf import DCFInput


def project_revenue(
    revenue: float,
    growth: float,
    years: int = 5,
):
    revenues = []

    current = revenue

    for _ in range(years):
        current *= (1 + growth)
        revenues.append(current)

    return revenues


def project_ebit(
    revenues: list[float],
    operating_margin: float,
):
    return [
        revenue * operating_margin
        for revenue in revenues
    ]


def project_nopat(
    ebits: list[float],
    tax_rate: float,
):
    return [
        ebit * (1 - tax_rate)
        for ebit in ebits
    ]

def project_fcf(
    nopats: list[float],
    revenues: list[float],
    capex_percent: float,
    nwc_percent: float,
):
    fcfs = []

    for nopat, revenue in zip(
        nopats,
        revenues,
    ):
        capex = revenue * capex_percent
        nwc = revenue * nwc_percent

        fcf = nopat - capex - nwc

        fcfs.append(fcf)

    return fcfs

def discount_fcfs(
    fcfs: list[float],
    wacc: float,
):
    discounted = []

    for year, fcf in enumerate(fcfs, start=1):
        pv = fcf / ((1 + wacc) ** year)
        discounted.append(pv)

    return discounted

def terminal_value(
    last_fcf: float,
    wacc: float,
    terminal_growth: float,
):
    return (
        last_fcf
        * (1 + terminal_growth)
        / (wacc - terminal_growth)
    )


def discount_terminal_value(
    terminal_value: float,
    wacc: float,
    years: int,
):
    return terminal_value / (
        (1 + wacc) ** years
    )


def enterprise_value(
    discounted_fcfs: list[float],
    discounted_terminal_value: float,
):
    return (
        sum(discounted_fcfs)
        + discounted_terminal_value
    )


def equity_value(
    enterprise_value: float,
    net_debt: float,
):
    return enterprise_value - net_debt


def intrinsic_value_per_share(
    equity_value: float,
    shares_outstanding: float,
):
    return equity_value / shares_outstanding