from app.core.session_vault import *
from app import misc


def check_session(sid):
    if get_session(sid) is None:
        return False
    return True


def start_session(user=''):
    sid = misc.get_random_string(15)
    while check_session(sid):
        sid = misc.get_random_string(15)
    session = create_session(sid)
    session.user = user
    return session


def end_session(sid):
    remove_session(sid)


def update_session(session):
    set_session(session)


def get_session_ids(user=None):
    return get_sessions(user, True)
