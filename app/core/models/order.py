from app import app
from app.core.models.сontragent import Contragent
from app.core.models.cart import Cart
from app.core.models.items.base import BaseItem
from app.core.models.user import User


class Order:
    def __init__(self):
        self.items = []
        self.contragent = None
        self.user = None
        self.comment = ""
        self._price = 0.0
        self.is_checked_out = False
        self.sale = 0  # decimal num, percents of sale

    @property
    def price(self) -> float:
        return self._price * (1 - self.sale)

    @staticmethod
    def create(cart: Cart, contragent: Contragent, comment: str) -> Order:
        order = Order()
        order.items = cart.items
        order.contragent = contragent
        order.comment = comment
        return order

    def checkout_order(self) -> None:
        if self.is_checked_out:
            raise OverflowError('Order is already checked out')
        for i in self.items:
            i: BaseItem
            i.checkout_item()

    def count_price(self) -> None:
        self._price = 0
        for i in self.items:
            i: BaseItem
            self._price += i.get_price()

    @staticmethod
    def create_from_db(data) -> Order:
        order = Order()
        cart = data['cart']
        contragent = data['contragent']
        user = data['user_id']
        order.comment = data['comment']
        order.is_checked_out = data['is_checked_out']
        order.sale = data['sale']
        order.cart = Cart.create_from_dict(cart)
        order.contragent = Contragent.create_from_dict(contragent)
        order.user_id = User.get(user).get_id()
        return order
