import app.core.utilities.session_utility as utility
from app.core.models.cart import Cart
from app.core.models.items.composite_item import CompositeItem
from app.core.models.selection import RVDSelection
from app.core.models.session import Session
from app.core.models.user import User
from app.core.utilities import contragent_utility, selection_utility
from app.core.utilities.common import *


def get_session(sid: str):
    return utility.get_session(sid)


def set_comment(sid: str, comment: str):
    session = utility.get_session(sid)
    session.comment = comment
    session.save()
    return session.dict


def get_comment(sid: str):
    return utility.get_session(sid).comment or ''


def remove_session(sid: str):
    utility.delete_session(sid)


def get_user_sessions(username: str) -> list:
    sessions = utility.get_user_sessions(username)
    res = []
    for i in sessions:
        res.append(i.get_safe())
    return res


def set_contragent(sid: str, cid: str):
    session = utility.get_session(sid)
    contragent = contragent_utility.get_contragent(cid)
    session.contragent = contragent
    session.save()


def get_contragent(sid: str):
    session = utility.get_session(sid)
    contragent = session.contragent
    return contragent.get_safe()


def del_contragent(sid: str):
    session = utility.get_session(sid)
    del session.contragent
    session.save()


def get_cart(sid: str):
    cart = utility.get_cart(sid)
    if cart is None:
        return document_to_dict(Cart())
    cart = cart.get_safe()
    return cart


def del_cart_item(sid: str, item_id: int):
    utility.del_cart_item(sid, item_id)
    return utility.get_cart(sid).get_safe()


def add_part_to_cart(sid: str):
    session = utility.get_session(sid)
    selection: RVDSelection = session.selection
    if session.cart is None:
        session.cart = Cart()
    session.cart.items.append(selection.part)
    del session.selection
    session.save()


def add_selection_to_cart(sid: str):
    session = utility.get_session(sid)
    selection: RVDSelection = session.selection
    selection_items = selection_utility.get_selected_items(selection)
    items = []
    for i in selection_items.values():
        items.append(i)
    item = CompositeItem()
    item.items = items
    item.price = selection.subtotal['price']
    item.total_price = selection.subtotal['total_price']
    item.amount = selection.subtotal['amount']
    item.name = selection.subtotal['name']
    if session.cart is None:
        session.cart = Cart()
    session.cart.items.append(item)
    del session.selection
    session.save()
