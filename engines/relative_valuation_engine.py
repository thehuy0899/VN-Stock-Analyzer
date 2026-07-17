def analyze(
    current_price,
    eps,
    book_value_per_share,
    enterprise_value,
    ebitda,
):
    
    print(">>> relative_valuation_engine NEW VERSION")
    print(current_price)
    print(eps)
    print(book_value_per_share)
    print(enterprise_value)
    print(ebitda)

    pe = None
    pb = None
    ev_ebitda = None

    if eps not in (None, 0):
        pe = current_price / eps

    if book_value_per_share not in (None, 0):
        pb = current_price / book_value_per_share

    if ebitda not in (None, 0):
        ev_ebitda = enterprise_value / ebitda

    result = {
        "status": "success",
        "pe": pe,
        "pb": pb,
        "ev_ebitda": ev_ebitda,
        "valuation": [],
    }

    if pe is not None:
        if pe < 10:
            result["valuation"].append("Undervalued (Low PE)")
        elif pe > 20:
            result["valuation"].append("Expensive (High PE)")

    if pb is not None:
        if pb < 1:
            result["valuation"].append("Undervalued (Low PB)")
        elif pb > 3:
            result["valuation"].append("Expensive (High PB)")

    if ev_ebitda is not None:
        if ev_ebitda < 8:
            result["valuation"].append("Undervalued (Low EV/EBITDA)")
        elif ev_ebitda > 15:
            result["valuation"].append("Expensive (High EV/EBITDA)")

    return result