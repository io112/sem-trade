from mongoengine import EmbeddedDocument, DictField

from app.core.models.items.base import BaseItem
from app.core.models.items.composite_item import CompositeItem
from app.core.models.items.empty_item import EmptyItem


class RVDSelection(EmbeddedDocument):
    param_name = "selection"
    items = DictField()
    subtotal = DictField()

    # def __init__(self, session: Session, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     selection = session.data.get(self.param_name, {})
    #     self.items = {}
    #     self.subtotal = {}
    #     for i in selection:
    #         if i == "subtotal" and selection[i]["amount"] is not None:
    #             self.subtotal["amount"] = selection[i]["amount"]
    #             continue
    #         item_type = selection[i].get("type", "")
    #         item = create_simple_item(item_type, i)
    #         item.create_from_dict(selection[i])
    #         self.items[i] = item

    def __getitem__(self, item: str) -> BaseItem:
        res = self.items.get(item)
        if res is not None:
            return res
        return EmptyItem()

    def __setitem__(self, key, value: BaseItem):
        self.items[key] = value

    def __get__(self, instance=None, owner=None) -> dict:
        res = {}
        for i in self.items:
            res.update(self.items[i].__get__())
        res.update(self.get_subtotal())
        return res

    def calc_subtotal(self):
        res = 0
        for i in self.items.values():
            res += i.get_price()
        return res

    def set_subtotal(self, subtotal: dict):
        self.subtotal = subtotal

    def get_subtotal(self):
        return {"subtotal": self.subtotal}

    def finish_selection(self) -> CompositeItem:
        if len(self.check_presence()) != 0:
            raise Exception('some of items not available')
        res = CompositeItem('rvd_item')
        res.items = self.items.values()
        res.amount = self.subtotal["amount"]
        res.name = self.subtotal['name']
        return res

    def check_presence(self) -> list:
        candidates = {}
        req_amounts = {}
        errors = []
        for key in self.items:
            i: BaseItem = self.items[key]
            if not i.candidate == {}:
                candidate = i.candidate
                cid = candidate["_id"]
                if cid not in candidates:
                    candidates[cid] = candidate
                    req_amounts[cid] = 0
                req_amounts[cid] += i.get_amount()
                req_amount = req_amounts[cid] * self.subtotal["amount"]
                if req_amount > int(candidate["amount"]):
                    errors.append(
                        f"не хватает материалов: {candidate['name']}, доступно: {candidate['amount']},"
                        f" требуется: {req_amount}.")
            else:
                errors.append(f'Выбраны не все компоненты.')
        return errors
