from app.core.models.session import Session
import app.core.utilities.session_utility as utility
from app.core.utilities import contragent_utility
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


def get_user_sessions(username: str):
    return utility.get_user_sessions(username)


def set_contragent(sid: str, cid: str):
    session = utility.get_session(sid)
    contragent = contragent_utility.get_contragent(cid)
    session.contragent = contragent
    session.save()


def get_contragent(sid: str):
    session = utility.get_session(sid)
    return document_to_dict(session.contragent)


def get_cart(sid: str):
    return utility.get_cart(sid)


def del_cart_item(sid: str, item_id: int):
    utility.del_cart_item(sid, item_id)
    return utility.get_cart(sid)
