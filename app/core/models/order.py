import copy
from dataclasses import dataclass

import pymongo
import pytz
from mongoengine import Document, StringField, ReferenceField, FloatField, BooleanField, EmbeddedDocumentField, \
    DateTimeField, IntField
from pytz import tzinfo
from datetime import timedelta

from app.core.models.cart import Cart
from app.core.models.items.base import BaseItem
from app.core.models.items.cart_item import CartItem
from app.core.models.items.composite_item import CompositeItem
from app.core.models.session import Session
from app.core.models.user import User
from app.core.models.сontragent import Contragent
from app.core.utilities.common import document_to_dict
from app.db import base as db
from app.db.variables import *
from datetime import datetime
import xml.etree.ElementTree as ET


class Order(Document):
    @dataclass
    class Status:
        STATUS_CREATED = 'Создан'
        STATUS_CHECKED_OUT = 'Проведен'
        STATUS_EXPORTED = 'Экспортирован'
        STATUS_CLOSED = 'Закрыт'

    order_num = StringField()
    status = StringField(default=Status.STATUS_CREATED)
    contragent = ReferenceField(Contragent)
    upd_num = StringField()
    user = ReferenceField(User)
    comment = StringField()
    _price = FloatField()
    is_checked_out = BooleanField()
    cart = EmbeddedDocumentField(Cart)
    time_created = DateTimeField()
    sale = IntField()  # decimal num, percents of sale

    def __init__(self, *args, **values):

        super().__init__(*args, **values)

    @property
    def price(self) -> float:
        return self._price * (1 - self.sale)

    @staticmethod
    def create(cart: Cart, contragent: Contragent, comment: str, user: str):
        order = Order()
        order.cart = cart
        order.contragent = contragent
        order.comment = comment
        order.time_created = datetime.now(pytz.timezone('Europe/Moscow'))
        order.user = user
        order.count_price()
        return order

    def get_safe(self):
        res = document_to_dict(self)
        res['cart'] = self.cart.get_safe()
        res['contragent'] = self.contragent.get_safe()
        res['_id'] = str(res['_id'])
        res['user'] = self.user.get_safe()
        return res

    @staticmethod
    def create_from_session(session: Session):
        comment = ''
        if 'cart' not in session.data or len(session.data['cart']) < 1:
            raise NotImplementedError('cart is incorrect')
        if 'comment' in session.data:
            comment = session.data['comment']
        cart = Cart.create_from_session(session)
        contragent = Contragent.create_from_session(session)
        user = session.user
        return Order.create(cart, contragent, comment, user)

    def checkout_order(self) -> None:
        if self.is_checked_out:
            raise OverflowError('Order is already checked out')
        for i in self.cart.items:
            i: BaseItem
            i.checkout_item()
        self.is_checked_out = True
        self.status = self.Status.STATUS_CHECKED_OUT
        self._save()

    def get_db_dict(self):
        res = copy.deepcopy(self.__dict__)
        res.update(self.cart.dict)
        res['contragent'] = self.contragent.__get__()
        if self._id is None:
            del res['_id']
        return res

    def get_dict(self):
        res = self.get_db_dict()
        res['_id'] = str(res['_id'])
        res['contragent'] = self.contragent.get()
        return res

    def _save(self):
        self.count_price()
        if self.order_num is None:
            num = int(self.find_last_order_num()[3:])
            self.order_num = 'РВ-' + str(num + 1)
        if self._id is None:
            self._id = db.insert(order_collection, self.get_db_dict())
        else:
            db.update(order_collection, {'_id': self._id}, {'$set': self.get_db_dict()})

    @staticmethod
    def find_last_order_num():
        last_num = db.find_one(order_collection, {}, fields=['order_num'], sorting=[('order_num', pymongo.DESCENDING)])
        return last_num['order_num']

    def aggregate_items(self):
        res = {}
        cart = self.cart
        items_list = []
        for i in cart.items:
            if type(i) is CompositeItem:
                items_list.extend(i.aggregate_items())
            else:
                items_list.append(i)
        for i in items_list:
            item_id = i.item.id
            if item_id not in res:
                res[item_id] = i
            else:
                res[item_id].amount += i.amount
        items_list = list(res.values())
        return items_list

    def create_xml_doc(self) -> ET:
        dt = pytz.timezone('Europe/Moscow').localize(self.time_created) + timedelta(hours=3)
        dt: datetime
        contragent_name = self.contragent.name + (' ' + self.contragent.surname if self.contragent.surname else '')
        res = ET.Element('Документ')
        ET.SubElement(res, 'Ид').text = self.order_num
        ET.SubElement(res, 'Номер').text = self.order_num
        ET.SubElement(res, 'Дата').text = dt.strftime("%Y-%m-%d")
        ET.SubElement(res, 'ХозОперация').text = 'Заказ товара'
        ET.SubElement(res, 'Роль').text = 'Продавец'
        ET.SubElement(res, 'Валюта').text = 'RUB'
        ET.SubElement(res, 'Курс').text = str(1.0000)
        ET.SubElement(res, 'Сумма').text = str(self.cart.subtotal)
        ET.SubElement(res, 'Время').text = dt.strftime('%H:%M:%S')
        contragents = ET.Element('Контрагенты')
        contragent = ET.Element('Контрагент')
        ET.SubElement(contragent, 'Ид').text = str(self.contragent.id)
        ET.SubElement(contragent, 'Наименование').text = contragent_name
        ET.SubElement(contragent, 'Роль').text = 'Покупатель'
        ET.SubElement(contragent, 'ПолноеНаименование').text = contragent_name
        contragents.append(contragent)
        res.append(contragents)
        items = ET.Element('Товары')
        for i in self.aggregate_items():
            i: CartItem
            for j in i.create_xml():
                items.append(j)
        res.append(items)

        recs = ET.Element('ЗначенияРеквизитов')
        rec1 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec1, 'Наименование').text = 'Метод оплаты'
        ET.SubElement(rec1, 'Значение').text = 'Cash on delivery (COD)'
        rec2 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec2, 'Наименование').text = 'Метод доставки'
        ET.SubElement(rec2, 'Значение').text = 'Самовывоз'
        rec3 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec3, 'Наименование').text = 'Адрес'
        ET.SubElement(rec3, 'Значение').text = 'Самовывоз'
        rec4 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec4, 'Наименование').text = 'Адрес доставки'
        ET.SubElement(rec4, 'Значение').text = 'Самовывоз'
        rec5 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec5, 'Наименование').text = 'Покупатель, контакты'
        ET.SubElement(rec5, 'Значение').text = 'Тест'
        rec6 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec6, 'Наименование').text = 'Статус заказа'
        ET.SubElement(rec6, 'Значение').text = 'Заказ принят, ожидается закупка'

        recs.append(rec1)
        recs.append(rec2)
        recs.append(rec3)
        recs.append(rec4)
        recs.append(rec5)
        recs.append(rec6)
        res.append(recs)
        return res
