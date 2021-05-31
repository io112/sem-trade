import app.db.variables as dbvars
from app.core.models.items.base import BaseItem


class Clutch(BaseItem):
    required_params = ["name"]
    collection = dbvars.clutch_collection
    NomenclatureType = 'Муфта'

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = self.get_param_name()

    @staticmethod
    def get_param_name() -> str:
        return "clutch"

    def get_filter_params(self) -> dict:
        dictvals = ["name",
                    "arm_type",
                    "diameter"]
        res = self.get_props(dictvals)
        res["amount"] = {'$gte': int(self.amount)}
        return res

    def get_item_params(self) -> list:
        return ["_id", "arm_type", "diameter",
                "measure", "name", "type", "price"]
