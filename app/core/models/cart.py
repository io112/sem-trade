from app.core.models.items.base import BaseItem
from app.core.models.session import Session
from app.core.models.utils import create_item
from app.core.sessions import update_session


class Cart:

    def __init__(self):
        self.items = []
        self.subtotal = 0.0

    def __getitem__(self, item: int) -> BaseItem:
        return self.items[item]

    def __setitem__(self, key: int, value: BaseItem):
        self.items[key] = value

    def __delitem__(self, key: int):
        if key < len(self.items):
            item = self.items[key]
            item: BaseItem
            item.unreserve_item()
            del self.items[key]

    def add(self, item: BaseItem) -> str:
        item.find_candidate()
        if item.finish_item() != 'success':
            return 'Item not valid: ' + item.outer_name
        error = item.reserve_item()
        if error != 'success':
            return error
        self.items.append(item)
        return 'success'

    def __get__(self, instance=None, owner=None) -> dict:
        items = []
        for i in self.items:
            i: BaseItem
            items.append(i.__get__())
        self.get_subtotal()
        cart = {'cart': {'items': items, 'subtotal': self.subtotal}}
        return cart

    def get_subtotal(self):
        subt = 0
        for i in self.items:
            i: BaseItem
            subt += i.final_price
        self.subtotal = subt

    @staticmethod
    def create_from_dict(cart_dict: dict):
        res = Cart()
        items = cart_dict['items']
        for i in items:
            elem = list(i.values())[0]
            item = create_item(elem['type'], elem['outer_name'])
            item.create_from_dict(elem)
            res.items.append(item)
        return res

    @staticmethod
    def create_from_session(session: Session):
        res = Cart()
        current_cart = session.data.get('cart')
        if current_cart is not None:
            res = Cart.create_from_dict(current_cart)
        return res

    def save(self, session: Session):
        session.add_data(self.__get__())
        update_session(session)
