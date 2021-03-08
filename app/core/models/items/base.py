from abc import ABC, abstractmethod

import app.db.base as db


class BaseItem(ABC):
    required_params = [""]
    collection = ""
    not_zero_amount = {'amount': {'$not': {'$eq': 0}}}

    def __init__(self, out_name: str):
        self.candidate = {}
        self.amount = 1
        self.outer_name = out_name

    def not_zero_prop(self, prop):
        res = None
        val = self.__dict__[prop]
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
                candidate = {}

    @abstractmethod
    def get_price(self) -> float:
        pass

    def create_from_dict(self, data: dict):
        for i in data:
            if self.__dict__.get(i) is not None:
                val = data[i]
                try:
                    val = float(val)
                except Exception:
                    pass
                self.__dict__[i] = val
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
            if self.__dict__[i] is None or self.__dict__[i] == "":
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
        return self.reserve_item_amount(self.amount)

    def reserve_item_amount(self, amount) -> str:
        fin_amount = self.candidate['amount'] - amount
        if fin_amount < 0:
            return 'not enough amount'
        if self.candidate == {}:
            print('Candidate not found')
            return 'No candidate found'
        else:
            self.update_item_amount(fin_amount)
            return 'success'

    def unreserve_item(self):
        return self.unreserve_item_amount(self.amount)

    def unreserve_item_amount(self, amount):
        if self.candidate == {}:
            print('Candidate not found')
            return 'No candidate found'
        else:
            self.update_item_amount(self.candidate['amount'] + amount)
            return 'success'

    def update_item_amount(self, new_amount) -> str:
        item_id = self.candidate['_id']
        q = {'_id': item_id}
        update_data = {'$set': {'amount': new_amount}}
        self.candidate['amount'] = new_amount
        db.update(self.collection, q, update_data)
        return 'success'
