from mongoengine import ListField, FloatField, EmbeddedDocument, GenericReferenceField, GenericEmbeddedDocumentField, \
    signals

from app.core.models.items.base import BaseItem
from app.core.models.utils import create_item
from app.core.utilities.common import document_to_dict


class Cart(EmbeddedDocument):
    items = ListField(GenericEmbeddedDocumentField())
    subtotal = FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, item: int) -> BaseItem:
        return self.items[item]

    def __setitem__(self, key: int, value: BaseItem):
        self.items[key] = value

    def __delitem__(self, key: int):
        if key < len(self.items):
            del self.items[key]

    def get_safe(self) -> dict:
        res = document_to_dict(self)
        for i in range(len(self.items)):
            res['items'][i] = self.items[i].get_safe()
        return res
