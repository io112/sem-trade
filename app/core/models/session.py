from datetime import datetime

import pytz
from mongoengine import Document, StringField, DateTimeField, DictField, EmbeddedDocumentField, signals, ReferenceField, \
    IntField

from app.core.models.cart import Cart
from app.core.models.selection import RVDSelection
from app.core.models.сontragent import Contragent
from app.core.utilities.common import document_to_dict

msk_timezone = pytz.timezone('Europe/Moscow')


def save_handler(event):
    """Signal decorator to allow use of callback functions as class decorators."""

    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator


@save_handler(signals.pre_save)
def update_modified(sender, document):
    document.last_modified = msk_timezone.localize(datetime.now())
    if document.cart:
        cart = document.cart
        price = 0
        for i in cart.items:
            price += i.final_price
        cart.subtotal = price


@update_modified.apply
class Session(Document):
    id = StringField(primary_key=True)
    user = StringField()
    last_modified = DateTimeField()
    data = DictField()
    selection = EmbeddedDocumentField(RVDSelection)
    contragent = ReferenceField(Contragent)
    cart = EmbeddedDocumentField(Cart)
    sale = IntField()
    comment = StringField()

    def get_safe(self) -> dict:
        session = document_to_dict(self)
        if session.get('contragent'):
            session['contragent'] = self.contragent.get_safe()
        if session.get('cart'):
            session['cart'] = self.cart.get_safe()
        return session

    @property
    def dict(self):
        return self.to_mongo().to_dict()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def add_data(self, data):
        self.data.update(data)

    def set_user(self, user):
        self.user = user

    def set_data(self, key, val):
        self.data[key] = val

    def remove_data(self, key):
        if key in self.data:
            del self.data[key]

    def to_dict(self):
        return {"_id": self.id,
                "user": self.user,
                "data": self.data,
                "last_modified": self.last_modified,
                }

    def get_id(self):
        return self.id

    def set_id(self, sid):
        self.id = sid

    def create_from_struct(self, struct):
        self.set_id(struct["_id"])
        self.data = struct["data"]
        self.last_modified = struct["last_modified"]
        self.user = struct["user"]
