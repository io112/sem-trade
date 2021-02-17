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
    def create_object(name: str) -> BaseItem:
        if name is None:
            name = ""
        for i in RVDSelection.objects:
            if i == name:
                return RVDSelection.objects[i]()
        return EmptyItem()

    def __init__(self, session: Session):
        selection = session.data.get(self.param_name)
        self.selection = {}
        self.items = {}
        self.subtotal = {}
        if selection is not None:
            self.selection = selection
        for i in self.selection:
            item_type = ""
            if self.selection[i] is not None:
                item_type = self.selection[i].get("type")
            item = self.create_object(item_type)
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

    def set_subtotal(self, subtotal: dict):
        self.subtotal = subtotal

    def get_subtotal(self):
        return {"subtotal": self.subtotal}
    # def get_price
