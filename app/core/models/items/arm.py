import app.db.variables as dbvars
from app.core.models.items.base import BaseItem


class Arm(BaseItem):
    required_params = ["diameter", "arm_type"]
    collection = dbvars.arm_collection
    MeasureCode = '006'
    MeasureName = 'Метр'
    MeasureInt = 'MTR'
    MeasureText = 'метров'
    NomenclatureType = 'Рукав'

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = self.get_param_name()

    def get_amount(self):
        return self.amount

    @staticmethod
    def get_param_name() -> str:
        return "arm"

    def get_selection_name(self) -> str:
        arm_type = self.parameters.get('arm_type', '')
        diameter = self.parameters.get('diameter', '')
        return f'{arm_type}x{diameter}'

    def get_filter_params(self) -> dict:
        dictvals = ["name",
                    "braid",
                    "arm_type",
                    "diameter"]
        res = self.get_props(dictvals)
        res["amount"] = {'$gte': self.amount}
        return res

    def get_item_params(self) -> list:
        return ["_id", "name", "diameter", "measure",
                "type", "price", "braid", "arm_type"]

    def get_clutch_params(self):
        dictvals = ["arm_type",
                    "diameter"]
        res = {}
        for i in dictvals:
            res.update(self.not_zero_prop(i))
        res.update(self.not_zero_amount)
        return res
