from typing import List

from mongoengine import *

from app.core.models.items.cart_item import CartItem
from app.core.utilities.common import document_to_dict


class CompositeItem(EmbeddedDocument):
    MeasureCode = '796'
    MeasureName = 'Штука'
    MeasureInt = 'PCE'
    MeasureText = 'штук'
    NomenclatureType = 'composite_item'
    items = ListField(EmbeddedDocumentField(CartItem))
    total_price = FloatField()
    name = StringField()
    price = FloatField()
    amount = IntField()

    def __init__(self, *args, **values):

        super().__init__(*args, **values)

    def get_safe(self) -> dict:
        res = document_to_dict(self)
        for i in range(len(self.items)):
            res['items'][i] = self.items[i].get_safe()
        return res

    @staticmethod
    def get_param_name() -> str:
        return 'composite_item'

    def aggregate_items(self) -> List[CartItem]:
        res = {}
        for i in self.items:
            if i.item is None:
                continue
            i: CartItem
            item_id = i.item.id
            if item_id not in res:
                res[item_id] = i
                res[item_id].amount = i.amount * self.amount
            else:
                res[item_id].amount += i.amount * self.amount
        items_list = list(res.values())
        return items_list

    def create_xml(self) -> list:
        items_list = self.aggregate_items()
        result = []
        for i in items_list:
            result.extend(i.create_xml(i.amount))
        return result
