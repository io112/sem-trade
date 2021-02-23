from app.core.models.items.base import BaseItem


class CompositeItem(BaseItem):

    def __init__(self, out_name: str):
        super().__init__(out_name)
        self.name = ""
        self.items = []

    @staticmethod
    def get_param_name() -> str:
        return 'composite_item'

    def get_filter_params(self) -> dict:
        dictvals = ["name"]
        return self.get_props(dictvals)

    def get_price(self) -> float:
        pass
