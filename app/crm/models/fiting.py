from app.crm.models.base import SiteObj
from app.crm.variables import fiting_cat_id


class Fiting(SiteObj):
    fiting_type_name = 'Тип фиттинга'
    diameter_name = 'Диаметр'
    carving_name = 'Резьба'


    def __init__(self):
        super().__init__()
        self.init_params()

    def init_params(self):
        self.type = 'fiting'
        self.category_id = fiting_cat_id

        self.diameter = 'Не задан'
        self.fiting_type = 'Не задан'
        self.carving = 'Не задан'


    def convert_to_dict(self):
        data = super().convert_to_dict()
        data['diameter'] = self.diameter
        data['fiting_type'] = self.fiting_type
        data['carving'] = self.carving

        return data

    @staticmethod
    def create_from_cml(obj):
        res = SiteObj.create_from_cml(obj)
        res.__class__ = Fiting
        res.init_params()

        req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
        for i in req:
            if i[1].text == Fiting.carving_name:
                res.carving = i[2].text
            elif i[1].text == Fiting.fiting_type_name:
                res.fiting_type = i[2].text
            elif i[1].text == Fiting.diameter_name:
                res.diameter = i[2].text
        return res
