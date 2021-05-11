from app import misc
from app.core.models.session import Session
from app.core.utilities import session_utility


def check_session(sid):
    if session_utility.get_session(sid) is None:
        return False
    return True


def start_session(user=''):
    sid = misc.get_random_string(15)
    while check_session(sid):
        sid = misc.get_random_string(15)
    session = Session()
    session.user = user
    Session.save()
    return session


def end_session(sid):
    session_utility.delete_session(sid)


# def update_session(session):
#     set_session(session)
#
#
# def get_session_ids(user=None):
#     return get_sessions(user, ['_id'])


# def get_user_sessions(user=None, fields=None):
#     return get_sessions(user, fields)
