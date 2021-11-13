from app.core.models.items.base import BaseItem


class GenericItem(BaseItem):
    crm_parameters = {}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = ''
        self.category_id = ''
        self.MeasureCode = '006'
        self.MeasureName = 'Метр'
        self.MeasureInt = 'MTR'
        self.MeasureText = 'метров'
        self.NomenclatureType = ''

    def get_selection_name(self) -> str:
        return f''
