from app.crm.models.base import SiteObj
from app.crm.variables import *


class Arm(SiteObj):
    diameter_name = 'Диаметр'
    vendor_name = 'Производитель'
    braid_name = 'Тип оплетки'

    def __init__(self):
        super().__init__()
        self.init_params()

    def init_params(self):
        self.category_id = arm_cat_id

        self.diameter = 'Не задан'
        self.vendor = 'Не задан'
        self.braid = 'Не задан'
        self.type = 'arm'

    def convert_to_dict(self):
        data = super().convert_to_dict()
        data['diameter'] = self.diameter
        data['vendor'] = self.vendor
        data['braid'] = self.braid
        return data

    @staticmethod
    def create_from_cml(obj):
        res = SiteObj.create_from_cml(obj)
        res.__class__ = Arm
        res.init_params()

        req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
        for i in req:
            if i[1].text == Arm.diameter_name:
                res.diameter = i[2].text
            elif i[1].text == Arm.vendor_name:
                res.vendor = i[2].text
            elif i[1].text == Arm.braid_name:
                res.braid = i[2].text
        return res
