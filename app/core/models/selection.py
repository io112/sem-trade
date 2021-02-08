from app.core.models.items.base import BaseItem
from app.core.models.items.empty_item import EmptyItem
from app.core.models.session import Session


class RVDSelection:
    param_name = "selection"

    def __init__(self, session: Session):
        selection = session.data.get(self.param_name)
        self.selection = {}
        self.items = {}
        # TODO: generate items
        if selection is not None:
            self.selection = selection

    def __getattr__(self, item: str) -> BaseItem:
        res = self.items.get(item)
        if res is not None:
            return res
        return EmptyItem()

    def __setattr__(self, key, value: BaseItem):
        self.items[key] = value

    def __get__(self, instance=None, owner=None) -> dict:
        res = {}
        for i in self.items:
            res.update(i.__get__())
        return res

    # def get_price
