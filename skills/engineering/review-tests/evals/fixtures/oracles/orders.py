ORDER_LIMIT = 4


def total(quantity, unit_price_cents):
    if not isinstance(quantity, int) or not 1 <= quantity <= ORDER_LIMIT:
        raise ValueError("quantity must be an integer from 1 through 4")
    return quantity * unit_price_cents
