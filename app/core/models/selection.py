from app.core.models.items.arm import Arm
from app.core.models.items.base import BaseItem
from app.core.models.items.clutch import Clutch
from app.core.models.items.empty_item import EmptyItem
from app.core.models.items.fiting import Fiting
from app.core.models.session import Session


class RVDSelection:
    param_name = "selection"
    objects = {Arm.get_param_name(): Arm, Clutch.get_param_name(): Clutch, Fiting.get_param_name(): Fiting}

    @staticmethod
    def create_object(name: str, out_name: str) -> BaseItem:
        if name is None:
            name = ""
        for i in RVDSelection.objects:
            if i == name:
                return RVDSelection.objects[i](out_name)
        return EmptyItem()

    def __init__(self, session: Session):
        selection = session.data.get(self.param_name)
        self.selection = {}
        self.items = {}
        self.subtotal = {}
        if selection is not None:
            self.selection = selection
        for i in self.selection:
            if i == "subtotal" and self.selection[i]["amount"] is not None:
                self.subtotal["amount"] = self.selection[i]["amount"]
                continue
            item_type = ""
            if self.selection[i] is not None:
                item_type = self.selection[i].get("type")
            item = self.create_object(item_type, i)
            item.create_from_dict(self.selection[i])
            self.items[i] = item

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
        return errors
