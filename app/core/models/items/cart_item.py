from mongoengine import EmbeddedDocument, GenericReferenceField, FloatField

from app.core.utilities.common import document_to_dict


class CartItem(EmbeddedDocument):
    item = GenericReferenceField()
    amount = FloatField()
    price = FloatField()
    total_price = FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_safe(self) -> dict:
        res = document_to_dict(self)
        res['item'] = self.item.get_safe()
        return res
