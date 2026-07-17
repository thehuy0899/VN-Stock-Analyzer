from vnstock import Quote


def load_market_data(symbol):
    symbol = symbol.upper().strip()

    q = Quote(
        symbol=symbol,
        source="VCI",
    )

    try:
        history = q.history(
            start="2025-01-01",
            end="2099-12-31",
        )

        latest = history.iloc[-1]

        current_price = (
            float(latest["close"])
            * 1000
        )

    except Exception:
        history = None
        current_price = None

    print(history.tail())
    print("Current Price:", current_price)

    return {
        "history": history,
        "current_price": current_price,
    }