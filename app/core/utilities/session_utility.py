from app.core.models.session import Session


def get_session(sid: str):
    return Session.objects(id=sid)[0]

