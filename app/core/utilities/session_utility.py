from app.core.models.session import Session
from app.core.utilities.common import *


def get_session(sid: str) -> Session:
    return Session.objects(id=sid)[0]


def delete_session(sid: str):
    session = get_session(sid)
    Session.delete(session)


def get_user_sessions(username: str):
    sessions = Session.objects(user=username)
    return queryset_to_list(sessions)


def get_cart(sid: str):
    session = get_session(sid)
    cart = session.cart
    if cart is None:
        return '{}'
    cart = document_to_dict(cart)
    return cart


def del_cart_item(sid: str, item_num: int):
    session = get_session(sid)
    del session.cart[item_num]
    session.save()
