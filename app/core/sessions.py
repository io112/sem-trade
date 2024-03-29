import random
import string

from app.core.models.session import Session
from app.core.utilities import session_utility


def get_random_string(length):
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def check_session(sid):
    if session_utility.get_session(sid) is None:
        return False
    return True


def start_session(user=''):
    sid = get_random_string(15)
    while check_session(sid):
        sid = get_random_string(15)
    session = Session(id=sid)
    session.user = user
    session.save()
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
