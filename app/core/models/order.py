import copy

import pytz
from pytz import tzinfo
from datetime import timedelta

from app.core.models.cart import Cart
from app.core.models.items.base import BaseItem
from app.core.models.session import Session
from app.core.models.сontragent import Contragent
from app.db import base as db
from app.db.variables import *
from datetime import datetime
import xml.etree.ElementTree as ET


class Order:
    def __init__(self):
        self._id = None
        self.contragent = None
        self.user = None
        self.comment = ""
        self._price = 0.0
        self.is_checked_out = False
        self.cart = None
        self.time_created = None
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
        order.time_created = datetime.now(pytz.timezone('Europe/Moscow'))
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

    def checkout_order(self) -> ET.Element:
        if self.is_checked_out:
            raise OverflowError('Order is already checked out')
        for i in self.cart.items:
            i: BaseItem
            i.checkout_item()
        self.is_checked_out = True
        self._save()
        return self.create_xml_doc()

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
        order.time_created = data['time_created']
        order._id = data['_id']
        order.cart = Cart.create_from_dict(cart)
        order.contragent = Contragent.create_from_dict(contragent)
        order.user_id = data['user']
        return order

    def get_db_dict(self):
        res = copy.deepcopy(self.__dict__)
        res.update(self.cart.dict)
        res['contragent'] = self.contragent.__get__()
        if self._id is None:
            del res['_id']
        return res

    def _save(self):
        if self._id is None:
            self._id = db.insert(order_collection, self.get_db_dict())
        else:
            db.update(order_collection, {'_id': self._id}, self.get_db_dict())

    def create_xml_doc(self) -> ET:
        dt = pytz.timezone('Europe/Moscow').localize(self.time_created) + timedelta(hours=3)
        dt: datetime
        res = ET.Element('Документ')
        ET.SubElement(res, 'Ид').text = 'РВ-29'
        ET.SubElement(res, 'Номер').text = 'РВ-29'
        ET.SubElement(res, 'Дата').text = dt.strftime("%Y-%m-%d")
        ET.SubElement(res, 'ХозОперация').text = 'Заказ товара'
        ET.SubElement(res, 'Роль').text = 'Продавец'
        ET.SubElement(res, 'Валюта').text = 'RUB'
        ET.SubElement(res, 'Курс').text = str(1.0000)
        ET.SubElement(res, 'Сумма').text = str(self.cart.subtotal)
        ET.SubElement(res, 'Время').text = dt.strftime('%H:%M:%S')
        contragents = ET.Element('Контрагенты')
        contragent = ET.Element('Контрагент')
        ET.SubElement(contragent, 'Ид').text = str(self.contragent._id)
        ET.SubElement(contragent, 'Наименование').text = str(self.contragent.name + ' ' + self.contragent.surname)
        ET.SubElement(contragent, 'Роль').text = 'Покупатель'
        ET.SubElement(contragent, 'ПолноеНаименование').text = str(self.contragent.name + ' ' + self.contragent.surname)
        contragents.append(contragent)
        res.append(contragents)
        items = ET.Element('Товары')
        for i in self.cart.items:
            i: BaseItem
            for j in i.create_xml():
                items.append(j)
        res.append(items)

        recs = ET.Element('ЗначенияРеквизитов')
        rec1 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec1, 'Наименование').text = 'Номер по 1С'
        ET.SubElement(rec1, 'Значение').text = 'РВ-23'
        rec2 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec2, 'Наименование').text = 'Дата по 1С'
        ET.SubElement(rec2, 'Значение').text = dt.strftime("%Y-%m-%dT%H:%M:%S")
        rec3 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec3, 'Наименование').text = 'ПометкаУдаления'
        ET.SubElement(rec3, 'Значение').text = 'false'
        rec4 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec4, 'Наименование').text = 'Статус заказа'
        ET.SubElement(rec4, 'Значение').text = 'Создан'
        recs.append(rec1)
        recs.append(rec2)
        recs.append(rec3)
        recs.append(rec4)
        res.append(recs)
        return res
