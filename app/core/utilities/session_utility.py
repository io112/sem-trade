from app.core.models.cart import Cart
from app.core.models.session import Session
from app.core.utilities.common import *


def get_session(sid: str) -> Session:
    return Session.objects(id=sid)[0] if len(Session.objects(id=sid)) > 0 else None


def delete_session(sid: str):
    session = get_session(sid)
    Session.delete(session)


def get_user_sessions(username: str) -> QuerySet:
    sessions = Session.objects(user=username).only('id', 'last_modified', 'user')
    return sessions


def get_cart(sid: str) -> Cart:
    session = get_session(sid)
    cart = session.cart
    return cart


def del_cart_item(sid: str, item_num: int):
    session = get_session(sid)
    del session.cart[item_num]
    session.save()
