from app.core.models.cart import Cart
from app.core.models.items.base import BaseItem
from app.core.models.session import Session
from app.core.models.сontragent import Contragent
from app.db import base as db
from app.db.variables import *


class Order:
    def __init__(self):
        self._id = None
        self.contragent = None
        self.user = None
        self.comment = ""
        self._price = 0.0
        self.is_checked_out = False
        self.cart = None
        self.sale = 0  # decimal num, percents of sale

    @property
    def price(self) -> float:
        return self._price * (1 - self.sale)

    @staticmethod
    def create(cart: Cart, contragent: Contragent, comment: str):
        order = Order()
        order.cart = cart
        order.contragent = contragent
        order.comment = comment
        return order

    @staticmethod
    def create_from_session(session: Session):
        comment = ''
        if 'cart' not in session.data or len(session.data['cart']) < 1:
            raise NotImplementedError('cart is incorrect')
        if 'comment' in session.data:
            comment = session.data['comment']
        cart = Cart.create_from_session(session)
        contragent = Contragent.create_from_session(session)
        return Order.create(cart, contragent, comment)

    def checkout_order(self) -> None:
        if self.is_checked_out:
            raise OverflowError('Order is already checked out')
        for i in self.cart.items:
            i: BaseItem
            i.checkout_item()
        self.is_checked_out = True

    def count_price(self) -> None:
        self._price = 0
        for i in self.cart.items:
            i: BaseItem
            self._price += i.get_price()

    @staticmethod
    def create_from_db(data):
        order = Order()
        cart = data['cart']
        contragent = data['contragent']
        order.comment = data['comment']
        order.is_checked_out = data['is_checked_out']
        order.sale = data['sale']
        order._id = data['_id']
        order.cart = Cart.create_from_dict(cart)
        order.contragent = Contragent.create_from_dict(contragent)
        order.user_id = data['user_id']
        return order

    def get_db_dict(self):
        res = self.__dict__
        res.update(self.cart.__get__())
        res['contragent'] = self.contragent.__get__()
        if self._id is None:
            del res['_id']
        return res

    def save(self):
        if self._id is None:
            db.insert(order_collection, self.get_db_dict())
        else:
            db.update(order_collection, {'_id': self._id}, self.get_db_dict())
