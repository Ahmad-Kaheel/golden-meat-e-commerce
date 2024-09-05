from voucher.models import Coupon
from order.models import OrderItems
from typing import NamedTuple, Optional


class CouponData(NamedTuple):
    coupons: Optional[Coupon] = None
    error: Optional[str] = None


def find_coupons(item: OrderItems) -> CouponData:
    try:
        item_coupons = item.product.coupon.all()
        return CouponData(coupons=item_coupons)
    except (Exception,):
        return CouponData(error='Coupons does not exist')
