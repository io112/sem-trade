from app.crm.models.base import SiteObj
from app.crm.variables import *


class Clutch(SiteObj):
    diameter_name = 'Диаметр'
    arm_type_name = 'Тип рукава'

    def __init__(self):
        super().__init__()
        self.init_params()

    def init_params(self):
        self.type = 'clutch'
        self.category_id = clutch_cat_id

        self.diameter = 'Не задан'
        self.arm_type = 'Не задан'

    def convert_to_dict(self):
        data = super().convert_to_dict()
        data['diameter'] = self.diameter
        data['arm_type'] = self.arm_type

        return data

    @staticmethod
    def create_from_cml(obj):
        res = SiteObj.create_from_cml(obj)
        res.__class__ = Clutch
        res.init_params()

        req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")

        for i in req:
            if i[1].text == Clutch.diameter_name:
                res.diameter = float(i[2].text)
            elif i[1].text == Clutch.arm_type_name:
                res.arm_type = i[2].text
        return res
