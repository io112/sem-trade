from abc import ABC, abstractmethod


class BaseItem(ABC):

    @property
    @abstractmethod
    def param_name(self) -> str: pass

    @abstractmethod
    def get_filter_params(self) -> dict: pass

    @abstractmethod
    def __getitem__(self, item: str) -> str: pass

    @abstractmethod
    def __setitem__(self, key: str, value: str): pass

    @abstractmethod
    def get_price(self) -> float: pass

    @abstractmethod
    def create_from_dict(self, data: dict): pass
