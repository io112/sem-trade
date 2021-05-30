from app.core.models.cart import Cart
from app.core.models.session import Session
from app.core.utilities.common import *


def get_session(sid: str) -> Session:
    return Session.objects(id=sid)[0] if len(Session.objects(id=sid)) > 0 else None


def delete_session(sid: str):
    session = get_session(sid)
    Session.delete(session)


def get_user_sessions(username: str, limit=None, offset=None, sorting=None) -> QuerySet:
    if username is not None:
        sessions = Session.objects(user=username)
    else:
        sessions = Session.objects
    if offset:
        sessions = sessions.skip(offset)
    if limit:
        sessions = sessions.limit(limit)
    if sorting:
        sessions = sessions.order_by(sorting)
    return sessions


def count_user_sessions(username: str = None):
    if username is not None:
        sessions = Session.objects(user=username)
    else:
        sessions = Session.objects
    return sessions.count()


def get_cart(sid: str) -> Cart:
    session = get_session(sid)
    cart = session.cart
    return cart


def del_cart_item(sid: str, item_num: int):
    session = get_session(sid)
    del session.cart[item_num]
    session.save()
