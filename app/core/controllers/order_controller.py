import locale
from typing import List

import pymongo
from bson import ObjectId
from flask import render_template

from app.api_views import msk_timezone
from app.core.controllers import session_controller
from app.core.models.order import Order
from app.core.models.user import User
from app.core.utilities import session_utility
from app.db import base as db
from app.db.variables import order_collection
import app.core.utilities.order_utility as utility
from app.core.utilities.common import *


def get_all_orders(user=None) -> list:
    res = []
    orders = utility.get_orders(user)
    if orders is None:
        return res
    for i in orders:
        res.append(i.get_safe())
    return res


def get_order(order_id) -> dict:
    return utility.get_order(order_id).get_safe()


def get_upd(order_id):
    order = utility.get_order(order_id)
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
    time = msk_timezone.localize(order.time_created)
    local_time = time.strftime("%d %B %Y г.")
    upd = render_template('UPD.htm', order=order.get_dict(),
                          items=order.cart.items,
                          date=local_time, day=time.strftime('%d'),
                          month=time.strftime('%B'),
                          year=time.strftime('%Y')[2:],
                          final_price=order._price)
    return upd


def set_upd(order_id, upd) -> dict:
    order_id = ObjectId(order_id)
    order = utility.get_order(order_id)
    order.upd_num = upd
    order.save()
    return get_id_safe_document(order)


def close_order(order_id) -> dict:
    order_id = ObjectId(order_id)
    order = utility.get_order(order_id)
    order.status = Order.Status.STATUS_CLOSED
    order.save()
    return get_id_safe_document(order)


def create_order(sid: str) -> Order:
    session = session_utility.get_session(sid)
    order = Order()
    order.cart = session.cart
    order.user = User.get_by_username(session.user)
    order.contragent = session.contragent
    order.comment = session.comment
    order._price = session.cart.subtotal
    order.sale = session.sale
    num = int(utility.find_last_order_num()[3:])
    order.order_num = 'РВ-' + str(num + 1)
    order.save()
    return order
