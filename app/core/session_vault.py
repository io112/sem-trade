import app.db.base as db
from app.core.models.session import Session

session_collection = 'session'


def get_session(sid) -> Session:
    query = {"_id": sid}
    res = db.find_one(session_collection, query)
    if res is None:
        return None
    session = Session()
    session.create_from_struct(res)
    return session


def set_session(session):
    session: Session
    query = {"_id": session.get_id()}
    res = db.replace_upsert(session_collection, query, session.to_dict())
    return res


def get_sessions(user=None, fields=None):
    query = {}
    f = None
    if user is not None:
        query = {"user": user}
    if fields is not None:
        f = {}
        for i in fields:
            f[i] = 1
    res = db.find(session_collection, query, f)
    return res


def create_session(sid):
    session = Session()
    session.set_id(sid)
    db.insert(session_collection, session.to_dict())
    return session


def remove_session(sid):
    db.remove(session_collection, {"_id": sid})
