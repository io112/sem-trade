from app.crm.models.base import SiteObj
from app.crm.variables import fiting_cat_id


class Fiting(SiteObj):
    clutch_type_name = 'Тип муфты'
    fiting_type_name = 'Тип фиттинга'
    fiting_kind_name = 'Вид фиттинга'
    diameter_name = 'Диаметр'
    size_name = 'Размер фиттинга'
    angle_name = 'Угол фиттинга'

    def __init__(self):
        super().__init__()
        self.category_id = fiting_cat_id
        self.init_params()

    def init_params(self):
        self.type = 'fiting'

        self.diameter = ''
        self.clutch_type = ''
        self.fiting_type = ''
        self.fiting_kind = ''
        self.size = ''
        self.angle = ''

    def convert_to_dict(self):
        data = super().convert_to_dict()
        data['clutch_type'] = self.clutch_type
        data['diameter'] = self.diameter
        data['fiting_type'] = self.fiting_type
        data['fiting_kind'] = self.fiting_kind
        data['size'] = self.size
        data['angle'] = self.angle
        return data

    @staticmethod
    def create_from_cml(obj):
        res = SiteObj.create_from_cml(obj)
        res.__class__ = Fiting
        res.init_params()

        req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
        for i in req:
            if i[1].text == Fiting.clutch_type_name:
                res.clutch_type = i[2].text
            elif i[1].text == Fiting.fiting_type_name:
                res.fiting_type = i[2].text
            elif i[1].text == Fiting.fiting_kind_name:
                res.fiting_kind = i[2].text
            elif i[1].text == Fiting.diameter_name:
                res.diameter = i[2].text
            elif i[1].text == Fiting.size_name:
                res.size = i[2].text
            elif i[1].text == Fiting.angle_name:
                res.angle = i[2].text
        return res
