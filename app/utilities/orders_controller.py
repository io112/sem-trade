from typing import List

import pymongo
from bson import ObjectId

from app.core.models.order import Order
from app.db import base as db
from app.db.variables import order_collection


def get_all_orders(user=None) -> List[dict]:
    q = {}
    res = []
    if user is not None:
        q = {'user': user}
    q = db.find(order_collection, q, sorting=[('order_num', pymongo.DESCENDING)])
    for i in q:
        res.append(Order.create_from_db(i).get_dict())
    return res


def get_order(order_id, user=None) -> dict:
    q = {'_id': ObjectId(order_id)}
    q = db.find_one(order_collection, q)
    if q is None:
        return None
    return Order.create_from_db(q).get_dict()
