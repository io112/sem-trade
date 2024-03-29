import datetime
import locale
from typing import List

import pytz
from bson import ObjectId
from flask import render_template

import app.core.utilities.order_utility as utility
from app.constants import *
from app.core.models.items.composite_item import CompositeItem
from app.core.models.order import Order
from app.core.models.user import User
from app.core.utilities import session_utility

msk_timezone = pytz.timezone('Europe/Moscow')


def get_all_orders(user=None, limit=None, offset=None, sorting=None) -> dict:
    res = []
    orders = utility.get_orders(user, limit, offset, sorting)
    if orders is None:
        return {}
    for i in orders:
        res.append(i.get_safe())
    count = utility.count_orders(user)
    from_elem = offset + 1
    to_elem = offset + (len(res) if limit else count)
    return {"from": from_elem, 'to': to_elem, 'count': count, 'data': res}


def check_presence(order_id: str) -> List[str]:
    order_id = ObjectId(order_id)
    res = []
    order = utility.get_order(order_id)
    for i in order.cart.items:
        if type(i) == CompositeItem:
            total_amount = i.amount
            for j in i.items:
                need_amount = j.amount * total_amount
                if j.item:
                    available_amount = j.item.amount
                    if need_amount > available_amount:
                        res.append(f'Не хватает {j.item.name} требуется: {need_amount}, '
                                   f'доступно: {available_amount}')
        else:
            need_amount = i.amount
            available_amount = i.item.amount
            if need_amount > available_amount:
                res.append(f'Не хватает {i.item.name} требуется: {need_amount}, '
                           f'доступно: {available_amount}')
    return res


def get_order(order_id) -> dict:
    return utility.get_order(order_id).get_safe()


def get_upd(order_id):
    order = utility.get_order(order_id)
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
    time = msk_timezone.localize(order.time_created)
    local_time = time.strftime("%d %B %Y г.")
    upd = render_template('UPD.htm',
                          order=order.get_safe(),
                          items=order.cart.items,
                          date=local_time, day=time.strftime('%d'),
                          month=time.strftime('%B'),
                          year=time.strftime('%Y')[2:],
                          total_price=order._price,
                          commit_hash=commit_hash)
    return upd


def get_bill(order_id):
    order = utility.get_order(order_id)
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
    time = msk_timezone.localize(datetime.datetime.now())
    local_time = time.strftime("%d %B %Y г.")
    bill = render_template('Bill.htm',
                           commit_hash=commit_hash,
                           order=order.get_safe(),
                           items=order.cart.items,
                           date=local_time, day=time.strftime('%d'),
                           month=time.strftime('%B'),
                           year=time.strftime('%Y')[2:],
                           total_price=order._price)
    return bill


def set_upd(order_id, upd) -> dict:
    order_id = ObjectId(order_id)
    order = utility.get_order(order_id)
    order.upd_num = upd
    order.save()
    return order.get_safe()


def close_order(order_id) -> List[str]:
    order_id = ObjectId(order_id)
    order = utility.get_order(order_id)
    if order.status == order.Status.STATUS_CREATED:
        raise ValueError('Заказ еще не проведен')
    if (order.status == order.Status.STATUS_CLOSED or
            order.status == order.Status.STATUS_EXPORTED):
        raise ValueError('Заказ уже закрыт')
    if order.upd_num is None:
        raise ValueError('Заполните номер УПД')
    order.status = Order.Status.STATUS_CLOSED
    order.save()
    return order.get_safe()


def checkout_order(order_id) -> Order:
    order = utility.get_order(ObjectId(order_id))
    if (order.status == order.Status.STATUS_CHECKED_OUT or
            order.status == order.Status.STATUS_CLOSED or
            order.status == order.Status.STATUS_EXPORTED):
        raise ValueError('Заказ уже проведен')
    missing_report = check_presence(order_id)
    if len(missing_report) > 0:
        raise ValueError('\r\n'.join(missing_report))
    for i in order.cart.items:
        if type(i) == CompositeItem:
            total_amount = i.amount
            for j in i.items:
                need_amount = j.amount * total_amount
                if j.item:
                    j.item.amount -= need_amount
                    j.item.save()
        else:
            need_amount = i.amount
            i.item.amount -= need_amount
            i.item.save()
    order.status = Order.Status.STATUS_CHECKED_OUT
    order.save()
    return order.get_safe()


def create_order(sid: str) -> Order:
    session = session_utility.get_session(sid)
    order = Order()
    if session.cart is None:
        raise ValueError('В корзине нет товаров')
    order.cart = session.cart
    order.user = User.get_by_username(session.user)
    order.contragent = session.contragent
    order.comment = session.comment
    order._price = session.cart.subtotal
    order.sale = session.sale
    order.time_created = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    num = utility.find_last_order_num()
    order.order_num = 'РВ-' + str(num + 1)
    order._number = num + 1
    order.save()
    return order
