from app.core.models.items.base import BaseItem


class EmptyItem(BaseItem):
    @property
    def param_name(self): return "None"

    def get_filter_params(self):
        return {}

    def __getitem__(self, item):
        return {}

    def __setitem__(self, key, value):
        pass

    def get_price(self):
        return 0

    def create_from_dict(self, data: dict):
        pass
