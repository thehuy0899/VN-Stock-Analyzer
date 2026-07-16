from vnstock import Vnstock


# ============================================================
# CAU HINH
# ============================================================

SYMBOL = "FPT"


# ============================================================
# LAY DU LIEU
# ============================================================

stock = Vnstock().stock(
    symbol=SYMBOL,
    source="VCI"
)

income = stock.finance.income_statement(
    period="year",
    lang="vi",
    dropna=True
)


# ============================================================
# HAM LAY CHI TIEU
# ============================================================

def get_item(item_id):
    data = income[
        income["item_id"] == item_id
    ]

    if data.empty:
        raise ValueError(
            f"Khong tim thay item_id: {item_id}"
        )

    return data


# ============================================================
# LAY CAC CHI TIEU TAI CHINH
# ============================================================

revenue = get_item("net_sales")

gross_profit = get_item("gross_profit")

operating_profit = get_item(
    "operating_profit_loss"
)

selling_expenses = get_item(
    "selling_expenses"
)

admin_expenses = get_item(
    "general_and_admin_expenses"
)


# ============================================================
# XAC DINH CAC NAM
# ============================================================

years = [
    column
    for column in income.columns
    if str(column).isdigit()
]

years = sorted(
    years,
    key=int
)


# ============================================================
# PHAN TICH BIEN LOI NHUAN
# ============================================================

print(
    f"\nPHAN TICH BIEN LOI NHUAN {SYMBOL}"
)

print("=" * 70)

gross_margins = {}
operating_margins = {}

selling_ratios = {}
admin_ratios = {}


for year in years:

    revenue_value = revenue[year].iloc[0]

    gross_profit_value = gross_profit[
        year
    ].iloc[0]

    operating_profit_value = operating_profit[
        year
    ].iloc[0]

    selling_value = abs(
        selling_expenses[year].iloc[0]
    )

    admin_value = abs(
        admin_expenses[year].iloc[0]
    )


    gross_margins[year] = (
        gross_profit_value
        / revenue_value
    ) * 100


    operating_margins[year] = (
        operating_profit_value
        / revenue_value
    ) * 100


    selling_ratios[year] = (
        selling_value
        / revenue_value
    ) * 100


    admin_ratios[year] = (
        admin_value
        / revenue_value
    ) * 100


    print(
        f"{year} | "
        f"Gross Margin: "
        f"{gross_margins[year]:.2f}% | "
        f"Operating Margin: "
        f"{operating_margins[year]:.2f}%"
    )


# ============================================================
# PHAT HIEN XU HUONG BIEN LOI NHUAN
# ============================================================

first_year = years[0]
latest_year = years[-1]


gross_margin_change = (
    gross_margins[latest_year]
    - gross_margins[first_year]
)


operating_margin_change = (
    operating_margins[latest_year]
    - operating_margins[first_year]
)


print("\nXU HUONG BIEN LOI NHUAN")

print("=" * 70)


print(
    f"Gross Margin: "
    f"{gross_margin_change:+.2f} diem %"
)


print(
    f"Operating Margin: "
    f"{operating_margin_change:+.2f} diem %"
)


# ============================================================
# PHAN TICH TY LE CHI PHI
# ============================================================

print("\nTY LE CHI PHI TREN DOANH THU")

print("=" * 70)


for year in years:

    print(
        f"{year} | "
        f"Selling/Revenue: "
        f"{selling_ratios[year]:.2f}% | "
        f"Admin/Revenue: "
        f"{admin_ratios[year]:.2f}%"
    )


selling_change = (
    selling_ratios[latest_year]
    - selling_ratios[first_year]
)


admin_change = (
    admin_ratios[latest_year]
    - admin_ratios[first_year]
)


print("\nTHAY DOI TY LE CHI PHI")

print("=" * 70)


print(
    f"Selling/Revenue: "
    f"{selling_change:+.2f} diem %"
)


print(
    f"Admin/Revenue: "
    f"{admin_change:+.2f} diem %"
)


# ============================================================
# ENGINE PHAN TICH
# ============================================================

print("\nKET LUAN TU DONG")

print("=" * 70)


if (
    gross_margin_change < 0
    and operating_margin_change > 0
):

    print(
        "PHAT HIEN NGHICH CHIEU BIEN LOI NHUAN."
    )

    print(
        "Bien loi nhuan gop suy giam "
        "nhung bien loi nhuan hoat dong tang."
    )


    if selling_change < 0:

        print(
            "- Ty le chi phi ban hang "
            "tren doanh thu giam."
        )


    if admin_change < 0:

        print(
            "- Ty le chi phi quan ly "
            "tren doanh thu giam."
        )


    if (
        selling_change < 0
        or admin_change < 0
    ):

        print(
            "Doanh nghiep dang cai thien "
            "hieu qua chi phi hoat dong."
        )

        print(
            "Day la mot trong cac yeu to "
            "ho tro Operating Margin."
        )


    else:

        print(
            "Chua tim thay bang chung "
            "cai thien chi phi hoat dong."
        )


else:

    print(
        "Khong phat hien nghich chieu "
        "bien loi nhuan."
    )