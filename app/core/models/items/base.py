from abc import ABC, abstractmethod

from mongoengine import Document
from mongoengine.fields import DictField, FloatField, StringField

import app.db.base as db
import xml.etree.ElementTree as ET


class BaseItem(Document):
    required_params = [""]
    collection = ""
    not_zero_amount = {'amount': {'$not': {'$eq': 0}}}
    MeasureCode = '796'
    MeasureName = 'Штука'
    MeasureInt = 'PCE'
    MeasureText = 'штук'
    NomenclatureType = ''
    candidate = DictField()
    parameters = DictField()
    amount = FloatField()
    final_price = FloatField()
    type = StringField()
    name = StringField()

    meta = {'allow_inheritance': True}

    def __init__(self, out_name: str):
        super().__init__()
        self.is_finish = False
        self.outer_name = out_name

    def not_zero_prop(self, prop):
        res = None
        val = self.parameters.get(prop)
        if val is not None and val != "":
            return {prop: val}
        return {}

    @staticmethod
    @abstractmethod
    def get_param_name() -> str:
        pass

    @abstractmethod
    def get_filter_params(self) -> dict:
        pass

    @abstractmethod
    def get_item_params(self) -> list:
        pass

    def __get__(self, instance=None, owner=None) -> dict:
        res = {}
        for i in self.__dict__:
            res.update(self.not_zero_prop(i))
        return {self.outer_name: res}

    def __getitem__(self, item: str) -> str:
        res = self.__dict__.get(item)
        if res is not None:
            return res
        return ""

    def __setitem__(self, key: str, value: str):
        self.__dict__[key] = value

    def find_candidate(self):
        if self.check_required_params():
            candidate = self.get_component(self.collection, self.get_filter_params())
            if candidate is not None:
                self.candidate = candidate
            else:
                self.candidate = {}

    def get_price(self) -> float:
        return self.get_price_for_amount(self.amount)

    def get_price_for_amount(self, amount) -> float:
        if self.candidate == {}:
            return 0
        return float(self.candidate["price"]) * amount

    def create_from_dict(self, data: dict):
        for i in data:
            if self.__dict__.get(i) is not None:
                val = data[i]
                try:
                    val = float(val)
                except Exception:
                    pass
                self.__dict__[i] = val
        if self.candidate == {}:
            self.find_candidate()

    @staticmethod
    def get_component_price(collection, component):
        res = BaseItem.get_component(collection, component)
        if res is None:
            return 0
        component_price = int(res["price"])
        return component_price

    @staticmethod
    def get_component(collection, component: dict) -> dict:
        res = db.join_queries_and_find(collection, component)
        if len(res) == 0:
            return None
        return res[0]

    def get_props(self, props_list: list) -> dict:
        res = {}
        for i in props_list:
            res.update(self.not_zero_prop(i))
        return res

    def check_required_params(self) -> bool:
        res = True
        for i in self.required_params:
            if self.parameters.get(i) is None or self.parameters.get(i) == "":
                res = False
        return res

    def check_validity(self) -> bool:
        res = self.check_required_params()
        if self.candidate == {}:
            return False
        return res

    def get_amount(self):
        return int(self.amount)

    def reserve_item(self) -> str:
        return self._reserve_item_amount(self.amount)

    def _reserve_item_amount(self, amount) -> str:
        self.find_candidate()
        fin_amount = self.candidate['amount'] - amount
        if fin_amount < 0:
            return 'not enough amount'
        if self.candidate == {}:
            print('Candidate not found')
            return 'No candidate found'
        else:
            self.__update_item_amount(amount * -1)
            return 'success'

    def unreserve_item(self):
        return self._unreserve_item_amount(self.amount)

    def _unreserve_item_amount(self, amount):
        self.find_candidate()
        if self.candidate == {}:
            print('Candidate not found')
            return 'No candidate found'
        else:
            self.__update_item_amount(amount)
            return 'success'

    def cancel_item(self):
        self.__update_reserved_amount(self.amount * -1)

    def _cancel_item_amount(self, amount):
        self.__update_reserved_amount(amount * -1)

    def checkout_item(self):
        self.__update_reserved_amount(self.amount * -1)

    def _checkout_item_amount(self, amount):
        self.__update_reserved_amount(amount * -1)

    def __update_reserved_amount(self, amount):
        item_id = self.candidate['_id']
        q = {'_id': item_id}
        update_data = {'$inc': {'reserved': amount}}
        db.update(self.collection, q, update_data)
        return 'success'

    def __update_item_amount(self, amount) -> str:
        item_id = self.candidate['_id']
        q = {'_id': item_id}
        update_data = {'$inc': {'amount': amount, 'reserved': -1 * amount}}
        db.update(self.collection, q, update_data)
        return 'success'

    def finish_item(self) -> str:
        if not self.check_validity():
            return 'Error: item not valid'
        self.is_finish = True
        for i in self.get_item_params():
            if self.candidate.get(i) is not None:
                self.__dict__[i] = self.candidate[i]
        self.final_price = self.get_price()
        return 'success'

    def create_xml(self, amount=-1) -> list:
        amount = self.amount if amount == -1 else amount
        res = ET.Element('Товар')
        ET.SubElement(res, 'Ид').text = str(self._id)
        ET.SubElement(res, 'Наименование').text = self.NomenclatureType
        measure = ET.Element('БазоваяЕдиница')
        measure.text = self.MeasureText
        measure.attrib['Код'] = self.MeasureCode
        measure.attrib['НаименованиеПолное'] = self.MeasureName
        measure.attrib['МеждународноеСокращение'] = self.MeasureInt
        res.append(measure)
        ET.SubElement(res, 'ЦенаЗаЕдиницу').text = str(self.get_price_for_amount(1))
        ET.SubElement(res, 'Количество').text = str(amount)
        ET.SubElement(res, 'Сумма').text = str(self.get_price_for_amount(amount))
        recs = ET.Element('ЗначенияРеквизитов')
        rec1 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec1, 'Наименование').text = 'ВидНоменклатуры'
        ET.SubElement(rec1, 'Значение').text = self.NomenclatureType
        rec2 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec2, 'Наименование').text = 'ТипНоменклатуры'
        ET.SubElement(rec2, 'Значение').text = 'Товар'
        recs.append(rec1)
        recs.append(rec2)
        res.append(recs)

        return [res]
