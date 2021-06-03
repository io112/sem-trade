import copy
from abc import abstractmethod

from mongoengine import Document, QuerySet
from mongoengine.fields import DictField, FloatField, StringField

import app.db.base as db
from app.core.utilities.common import document_to_dict


class ItemsQuerySet(QuerySet):

    def convert_dict(self, params_dict: dict):
        collection_name = 'parameters'
        res = {}
        for k in params_dict.keys():
            res[f'{collection_name}.{k}'] = params_dict[k]
        return res

    def filter_params(self, params_dict: dict):
        filter_dict = copy.deepcopy(params_dict)
        if 'amount' in filter_dict:
            del filter_dict['amount']
        if 'type' in filter_dict:
            del filter_dict['type']
        if 'part_name' in filter_dict:
            del filter_dict['part_name']
        if 'id' in filter_dict:
            query_filter = {'_id': filter_dict['id']}
        else:
            query_filter = self.convert_dict(filter_dict)
        return self.filter(__raw__=query_filter)


class BaseItem(Document):
    required_params = [""]
    collection = ""
    not_zero_amount = {'amount': {'$not': {'$eq': 0}}}
    MeasureCode = '796'
    MeasureName = 'Штука'
    MeasureInt = 'PCE'
    MeasureText = 'штук'
    NomenclatureType = ''
    id = StringField(primary_key=True)
    category_id = StringField()
    parameters = DictField()
    amount = FloatField()
    type = StringField()
    name = StringField()
    price = FloatField()
    measure = StringField()

    meta = {'abstract': True, 'queryset_class': ItemsQuerySet,
            'indexes': [
                {'fields': ['$name', "$price"],
                 'default_language': 'english',
                 'name': 'search_idx',
                 'weights': {'name': 1}
                 }
            ]
            }

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.is_finish = False

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

    def get_safe(self) -> dict:
        res = document_to_dict(self)
        return res

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
        self.total_price = self.get_price()
        return 'success'
