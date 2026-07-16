from vnstock import Vnstock

stock = Vnstock().stock(
    symbol="FPT",
    source="VCI"
)

income = stock.finance.income_statement(
    period="year",
    lang="vi",
    dropna=True
)

# =====================================
# TỰ ĐỘNG TÌM CÁC NĂM
# =====================================

year_columns = [
    column
    for column in income.columns
    if str(column).isdigit()
]

years = sorted(
    year_columns,
    key=int,
    reverse=True
)

print("CAC NAM TIM DUOC:")
print(years)

# =====================================
# TÌM CHỈ TIÊU
# =====================================

revenue_row = income[
    income["item_id"] == "net_sales"
]

profit_row = income[
    income["item_id"]
    == "attributable_to_parent_company"
]

# =====================================
# LẤY NĂM MỚI NHẤT VÀ NĂM TRƯỚC
# =====================================

latest_year = years[0]
previous_year = years[1]
oldest_year = years[-1]

# =====================================
# LẤY SỐ LIỆU
# =====================================

latest_revenue = revenue_row[
    latest_year
].iloc[0]

previous_revenue = revenue_row[
    previous_year
].iloc[0]

oldest_revenue = revenue_row[
    oldest_year
].iloc[0]

latest_profit = profit_row[
    latest_year
].iloc[0]

previous_profit = profit_row[
    previous_year
].iloc[0]

oldest_profit = profit_row[
    oldest_year
].iloc[0]

# =====================================
# TĂNG TRƯỞNG NĂM GẦN NHẤT
# =====================================

revenue_growth = (
    latest_revenue / previous_revenue - 1
) * 100

profit_growth = (
    latest_profit / previous_profit - 1
) * 100

# =====================================
# TÍNH CAGR
# =====================================

number_of_years = (
    int(latest_year) - int(oldest_year)
)

revenue_cagr = (
    (
        latest_revenue / oldest_revenue
    ) ** (1 / number_of_years)
    - 1
) * 100

profit_cagr = (
    (
        latest_profit / oldest_profit
    ) ** (1 / number_of_years)
    - 1
) * 100

# =====================================
# HIỂN THỊ KẾT QUẢ
# =====================================

print("\nPHAN TICH FPT")
print("=" * 50)

print(
    "Nam moi nhat:",
    latest_year
)

print(
    "Nam cu nhat:",
    oldest_year
)

print()

print(
    f"Tang truong doanh thu {latest_year}:",
    f"{revenue_growth:.2f}%"
)

print(
    f"CAGR doanh thu {number_of_years} nam:",
    f"{revenue_cagr:.2f}%"
)

print()

print(
    f"Tang truong LNST {latest_year}:",
    f"{profit_growth:.2f}%"
)

print(
    f"CAGR LNST {number_of_years} nam:",
    f"{profit_cagr:.2f}%"
)