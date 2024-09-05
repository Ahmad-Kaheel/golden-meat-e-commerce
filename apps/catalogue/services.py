from decimal import Decimal

def get_discount(price, discount):
    """Calculating discount"""

    discount_amount = (price * Decimal(discount) / Decimal(100))
    total = price - discount_amount
    int_total = int(total)
    return int_total
