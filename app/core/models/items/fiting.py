import app.db.variables as dbvars
from app.core.models.items.base import BaseItem


class Fiting(BaseItem):
    required_params = ["name"]
    collection = dbvars.fiting_collection
    NomenclatureType = 'Фитинг'

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = self.get_param_name()

    @staticmethod
    def get_param_name() -> str:
        return "fiting"

    def get_selection_name(self) -> str:
        type = self.parameters.get('fiting_type', '')
        carving = self.parameters.get('carving', '')
        return f'({type} {carving})'

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
