from app.core.models.items.base import BaseItem
from app.crm.meta import *


class Pipe(BaseItem):
    crm_parameters = {'Размер': 'size'}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = PIPE_PARAM_NAME
        self.category_id = PIPE_CAT_ID
        self.MeasureCode = '006'
        self.MeasureName = 'Метр'
        self.MeasureInt = 'MTR'
        self.MeasureText = 'метров'
        self.NomenclatureType = PIPE_NOMENCLATURE_TYPE

    def get_selection_name(self) -> str:
        return f''
