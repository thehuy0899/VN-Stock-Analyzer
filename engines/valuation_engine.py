from core.valuation import Valuation


def load_valuation(
    price: float,
    eps: float,
    book_value: float,
):
    return Valuation(
        pe=price / eps if eps else 0,
        pb=price / book_value if book_value else 0,
        eps=eps,
        book_value=book_value,
        price=price,
    )