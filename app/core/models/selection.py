from mongoengine import EmbeddedDocument, DictField, EmbeddedDocumentField, ListField, StringField

from app.core.models.items.cart_item import CartItem
from app.core.utilities.common import document_to_dict


class RVDSelection(EmbeddedDocument):
    param_name = "selection"
    items = ListField()
    subtotal = DictField()
    job_type = StringField()
    part = EmbeddedDocumentField(CartItem)

    def get_safe(self):
        res = document_to_dict(self)
        res['items'] = []
        for i in self.items:
            res['items'].append(i.get_safe())
        if self.part:
            res['part'] = self.part.get_safe()
        return res
