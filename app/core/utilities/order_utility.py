from app.core.models.order import Order
from app.core.models.user import User


def get_orders(user=None):
    if user is not None:
        user = User.get_by_username(user)
        return Order.objects(user=user)
    return Order.objects


def get_order(order_id):
    return Order.objects(id=order_id)[0]


def find_last_order_num():
    last_num = Order.objects().order_by('-order_num').only('order_num')
    if last_num.count() == 0 or last_num[0].order_num is None:
        return 'РВ-0'
    return last_num[0].order_num
