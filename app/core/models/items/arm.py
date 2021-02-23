from app.core.models.items.base import BaseItem
import app.db.variables as dbvars


class Arm(BaseItem):
    required_params = ["diameter", "arm_type"]
    collection = dbvars.arm_collection

    def __init__(self, out_name):
        super().__init__(out_name)
        self.amount = 1
        self.name = ""
        self.length = 0
        self.braid = ""
        self.arm_type = ""
        self.diameter = ""
        self.type = self.get_param_name()

    def get_amount(self):
        return int(self.length) * int(self.amount)

    @staticmethod
    def get_param_name() -> str:
        return "arm"

    def get_filter_params(self) -> dict:
        dictvals = ["name",
                    "braid",
                    "arm_type",
                    "diameter"]
        res = self.get_props(dictvals)
        res["amount"] = {'$gte': int(self.length) * int(self.amount)}
        return res

    def get_price(self) -> float:
        length = 0
        if self["length"] != "":
            length = float(self["length"])

        if self.candidate == {}:
            return 0

        res = float(self.candidate["price"]) * length
        return res

    def get_clutch_params(self):
        dictvals = ["arm_type",
                    "diameter"]
        res = {}
        for i in dictvals:
            res.update(self.not_zero_prop(i))
        res.update(self.not_zero_amount)
        return res
