from vnstock import Vnstock

stock = Vnstock().stock(
    symbol="FPT",
    source="VCI"
)

data = stock.quote.history(
    start="2026-07-01",
    end="2026-07-14"
)

print(data)