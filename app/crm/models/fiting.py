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

    @staticmethod
    def create_from_cml(obj):
        res = SiteObj.create_from_cml(obj)
        res.__class__ = Fiting
        res.init_params()

        req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
        for i in req:
            if i[1].text == Fiting.carving_name:
                res.parameters['carving'] = i[2].text
            elif i[1].text == Fiting.fiting_type_name:
                res.parameters['fiting_type'] = i[2].text
            elif i[1].text == Fiting.diameter_name:
                res.parameters['diameter'] = float(i[2].text)
        return res
