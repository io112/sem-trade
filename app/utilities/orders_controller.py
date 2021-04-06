from typing import List

from app.core.models.order import Order
from app.db import base as db
from app.db.variables import order_collection


def get_all_orders() -> List[Order]:
    q = db.find(order_collection, {})
    res = []
    for i in q:
        res.append(Order.create_from_db(i))
    return res
