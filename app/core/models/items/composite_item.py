from typing import List

from mongoengine import ListField, FloatField, StringField, EmbeddedDocument, IntField, \
    EmbeddedDocumentField

from app.core.models.items.base import BaseItem
from app.core.models.items.cart_item import CartItem
from app.core.models.utils import create_simple_item
# noinspection SpellCheckingInspection
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

    def get_filter_params(self) -> dict:
        dictvals = ["name"]
        return self.get_props(dictvals)

    def get_price(self) -> float:
        res = 0
        for i in self.items:
            i: BaseItem
            res += i.get_price()
        return res * self.amount

    def create_from_dict(self, data: dict):
        for i in data:
            if i == 'items':
                self.process_items(data[i])
            elif self.__dict__.get(i) is not None:
                self.__dict__[i] = data[i]

    def process_items(self, items: dict):
        for item in items:
            item_type = items[item]['type']
            res = create_simple_item(item_type, item)
            res.create_from_dict(items[item])
            self.items.append(res)

    def aggregate_items(self) -> List[CartItem]:
        res = {}
        for i in self.items:
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
