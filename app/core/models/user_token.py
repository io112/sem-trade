import secrets
from datetime import datetime

from mongoengine import Document, ReferenceField, StringField, DateTimeField, signals

from app.core.models.user import User


def save_handler(event):
    """Signal decorator to allow use of callback functions as class decorators."""

    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator


@save_handler(signals.post_init)
def update_created(sender, document):
    document.created_at = datetime.now()
    token = secrets.token_urlsafe(128)
    while UserToken.objects(token=token).count() != 0:
        token = secrets.token_urlsafe(128)
    document.token = token


@update_created.apply
class UserToken(Document):
    user = ReferenceField(User)
    token = StringField()
    created_at = DateTimeField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
