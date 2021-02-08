from app.core.models.items.base import BaseItem


class Arm(BaseItem):

    def __init__(self):
        self.name = ""
        self.length = ""
        self.braid = ""
        self.arm_type = ""
        self.diameter = ""

    @property
    def param_name(self) -> str: return "Arm"

    def get_filter_params(self) -> dict:
        return {"name": self.name,
                "braid": self.braid,
                "arm_type": self.arm_type,
                "diameter": self.diameter,
                }

    def __getitem__(self, item: str) -> str:
        res = self.__dict__[item]
        if res is not None:
            return res
        return ""

    def __setitem__(self, key: str, value: str):
        self.__dict__[key] = value

    def get_price(self) -> float:
        pass

    def create_from_dict(self, data: dict):
        pass
