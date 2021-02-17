from abc import ABC, abstractmethod

import app.db.base as db


class BaseItem(ABC):

    def __init__(self, out_name: str):
        self.outer_name = out_name

    def not_zero_prop(self, prop):
        res = None
        val = self.__dict__[prop]
        if val is not None and val != "":
            return {prop: val}
        return {}

    @staticmethod
    @abstractmethod
    def get_param_name() -> str: pass

    @abstractmethod
    def get_filter_params(self) -> dict: pass

    @abstractmethod
    def __get__(self, instance=None, owner=None) -> dict: pass

    @abstractmethod
    def __getitem__(self, item: str) -> str: pass

    @abstractmethod
    def __setitem__(self, key: str, value: str): pass

    @abstractmethod
    def get_price(self) -> float: pass

    @abstractmethod
    def create_from_dict(self, data: dict): pass

    @staticmethod
    def get_component_price(collection, component):
        res = BaseItem.get_component(collection, component)
        if res is None:
            return 0
        component_price = int(res["price"])
        return component_price

    @staticmethod
    def get_component(collection, component: dict):
        res = db.join_queries_and_find(collection, component)
        if len(res) == 0:
            return None
        return res[0]
