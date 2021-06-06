import app.core.utilities.session_utility as utility
from app.core.models.cart import Cart
from app.core.models.items.composite_item import CompositeItem
from app.core.models.selection import RVDSelection
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
    session = utility.get_session(sid)
    if session:
        return session.comment or ''
    return ''


def remove_session(sid: str):
    utility.delete_session(sid)


def get_user_sessions(username: str, limit=0, offset=0, sorting='-last_modified') -> dict:
    sessions = utility.get_user_sessions(username, limit, offset, sorting)
    res = []
    for i in sessions:
        res.append(i.get_safe())
    count = utility.count_user_sessions(username)
    from_elem = offset + 1
    to_elem = offset + (len(res) if limit else count)
    res = {"from": from_elem, 'to': to_elem, 'count': count, 'data': res}
    return res


def set_contragent(sid: str, cid: str):
    session = utility.get_session(sid)
    contragent = contragent_utility.get_contragent(cid)
    session.contragent = contragent
    session.save()


def get_contragent(sid: str):
    session = utility.get_session(sid)
    contragent = session.contragent
    if contragent:
        return contragent.get_safe()
    else:
        return {}


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
    if selection.part is None:
        raise ValueError('Запчасть не выделена')
    if selection.part.amount <= 0:
        raise ValueError('Выбрано 0 или меньше предметов')
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
    if not selection.subtotal['job_type']:
        raise ValueError(f'Выберите тип рукава')
    for i in selection_items.values():
        if i.amount <= 0:
            raise ValueError(f'Выбрано 0 или меньше предметов: {i.name}')
        items.append(i)
    if len(items) != len(selection.items):
        raise ValueError('Выбраны не все компоненты')
    item = CompositeItem()
    item.items = items
    item.price = selection.subtotal['price']
    item.total_price = selection.subtotal['total_price']
    item.amount = selection.subtotal['amount']
    item.name = selection.subtotal['name']
    if not item.amount:
        raise ValueError(f'Выбрано 0 или меньше РВД')
    if session.cart is None:
        session.cart = Cart()
    session.cart.items.append(item)
    del session.selection
    session.save()
