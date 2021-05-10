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

    @staticmethod
    def create_from_cml(obj):
        res = SiteObj.create_from_cml(obj)
        res.__class__ = Clutch
        res.init_params()

        req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")

        for i in req:
            if i[1].text == Clutch.diameter_name:
                res.parameters['diameter'] = float(i[2].text)
            elif i[1].text == Clutch.arm_type_name:
                res.parameters['arm_type'] = i[2].text
        return res
