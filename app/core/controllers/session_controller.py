from app.core.models.session import Session
import app.core.utilities.session_utility as utility


def set_comment(sid: str, comment: str):
    session = utility.get_session(sid)
    session.comment = comment
    session.save()
    return session.dict


def get_comment(sid: str):
    return utility.get_session(sid).comment or ''
