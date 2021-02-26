from app.core.models.items.base import BaseItem


class Cart:

    def __init__(self):
        self.items = []

    def __getitem__(self, item: int) -> BaseItem:
        return self.items[item]

    def __setitem__(self, key: int, value: BaseItem):
        self.items[key] = value

    def add(self, item: BaseItem):
        self.items.append(item)

    def __get__(self, instance=None, owner=None):
        items = {}
        for i in self.items:
            i: BaseItem
            items.update(i.__get__())
        cart = {'cart': {'items': items}}

    @staticmethod
    def create_from_dict(cart_dict: dict):
        res = Cart()
        items = cart_dict['items']
        for i in items:
            item = BaseItem(i)
            item.create_from_dict(items[i])
            res.add(item)
        return res
