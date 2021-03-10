from app.core.models.items.base import BaseItem
import app.db.variables as dbvars


class Fiting(BaseItem):
    required_params = ["name"]
    collection = dbvars.fiting_collection

    def __init__(self, out_name):
        super().__init__(out_name)
        self.amount = 1
        self.carving = ""
        self.diameter = ""
        self.name = ""
        self.fiting_type = ""
        self.type = self.get_param_name()

    @staticmethod
    def get_param_name() -> str:
        return "fiting"

    def get_filter_params(self) -> dict:
        dictvals = ["name",
                    "carving",
                    "fiting_type",
                    "diameter"]
        res = self.get_props(dictvals)
        res["amount"] = {'$gte': int(self.amount)}
        return res

    def get_item_params(self) -> list:
        return ["_id", "carving", "diameter", "fiting_type", "measure", "name", "type",
                "price"]
