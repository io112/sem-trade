import app.db.variables as dbvars
from app.core.models.items.base import BaseItem
from app.crm.meta import *


class Clutch(BaseItem):
    crm_parameters = {'Диаметр': 'diameter', 'Тип рукава': 'arm_type'}
    collection = dbvars.clutch_collection

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = CLUTCH_PARAM_NAME
        self.category_id = CLUTCH_CAT_ID
        self.NomenclatureType = CLUTCH_NOMENCLATURE_TYPE

    def get_selection_name(self) -> str:
        return ''
