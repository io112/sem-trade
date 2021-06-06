from mongoengine import EmbeddedDocument, DictField, EmbeddedDocumentField

from app.core.models.items.cart_item import CartItem
from app.core.utilities.common import document_to_dict


class RVDSelection(EmbeddedDocument):
    param_name = "selection"
    items = DictField()
    subtotal = DictField()
    part = EmbeddedDocumentField(CartItem)

    def get_safe(self):
        res = document_to_dict(self)
        if self.part:
            res['part'] = self.part.get_safe()
        return res
