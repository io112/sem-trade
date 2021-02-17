from app.core.models.items.base import BaseItem
import app.db.variables as dbvars


class Arm(BaseItem):

    def __init__(self, out_name):
        super().__init__(out_name)
        self.name = ""
        self.length = "0"
        self.braid = ""
        self.arm_type = ""
        self.diameter = ""
        self.type = self.get_param_name()

    @staticmethod
    def get_param_name() -> str:
        return "arm"

    def __get__(self, instance=None, owner=None) -> dict:
        res = {}
        for i in self.__dict__:
            res.update(self.not_zero_prop(i))
        return {self.outer_name: res}

    def get_filter_params(self) -> dict:
        dictvals = ["name",
                    "braid",
                    "arm_type",
                    "diameter"]
        res = {}
        for i in dictvals:
            res.update(self.not_zero_prop(i))
        return res

    def __getitem__(self, item: str) -> str:
        res = self.__dict__.get(item)
        if res is not None:
            return res
        return ""

    def __setitem__(self, key: str, value: str):
        self.__dict__[key] = value

    def get_price(self) -> float:
        length = 0
        if self["length"] != "":
            length = float(self["length"])

        return float(self.get_component_price(dbvars.arm_collection,
                                              self.get_filter_params())) \
               * length

    def create_from_dict(self, data: dict):
        for i in data:
            if self.__dict__.get(i) is not None:
                self.__dict__[i] = data[i]

    def get_clutch_params(self):
        dictvals = ["arm_type",
                    "diameter"]
        res = {}
        for i in dictvals:
            res.update(self.not_zero_prop(i))
        return res
