from app.core.models.order import Order
from app.core.models.user import User


def get_orders(user=None, limit=None, offset=None, sorting='-number'):
    if user is not None:
        user = User.get_by_username(user)
        res = Order.objects(user=user)
    else:
        res = Order.objects
    if offset:
        res = res.skip(offset)
    if limit:
        res = res.limit(limit)
    return res.order_by(sorting)


def count_orders(user=None):
    if user is not None:
        user = User.get_by_username(user)
        res = Order.objects(user=user)
    else:
        res = Order.objects
    return res.count()


def get_order(order_id):
    return Order.objects(id=order_id)[0]


def find_last_order_num():
    last_num = Order.objects().order_by('-_number').only('_number')
    if last_num.count() == 0 or last_num[0]._number is None:
        return 0
    return last_num[0]._number
