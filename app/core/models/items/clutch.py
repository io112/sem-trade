from app.core.models.items.base import BaseItem
import app.db.variables as dbvars


class Clutch(BaseItem):
    required_params = ["name"]
    collection = dbvars.clutch_collection

    def __init__(self, out_name):
        super().__init__(out_name)
        self.amount = 1
        self.name = ""
        self.arm_type = ""
        self.diameter = ""
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

    def get_price(self) -> float:
        if self.candidate == {}:
            return 0
        return float(self.candidate["price"])
