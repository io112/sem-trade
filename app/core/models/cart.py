from app.core.models.items.base import BaseItem
from app.core.models.session import Session
from app.core.models.utils import create_item


class Cart:

    def __init__(self):
        self.items = []

    def __getitem__(self, item: int) -> BaseItem:
        return self.items[item]

    def __setitem__(self, key: int, value: BaseItem):
        self.items[key] = value

    def add(self, item: BaseItem) -> str:
        item.find_candidate()
        if not item.check_validity():
            return 'Item not valid: ' + item.outer_name
        error = item.reserve_item()
        if error != 'success':
            return error
        self.items.append(item)
        return 'success'

    def __get__(self, instance=None, owner=None):
        items = []
        for i in self.items:
            i: BaseItem
            items.append(i.__get__())
        cart = {'cart': {'items': items}}
        return cart

    @staticmethod
    def create_from_dict(cart_dict: dict):
        res = Cart()
        items = cart_dict['items']
        for i in items:
            elem = list(i.values())[0]
            item = create_item(elem['type'], elem['outer_name'])
            item.create_from_dict(elem)
            res.add(item)
        return res

    @staticmethod
    def create_from_session(session: Session):
        res = Cart()
        current_cart = session.data.get('cart')
        if current_cart is not None:
            res = Cart.create_from_dict(current_cart)
        return res
