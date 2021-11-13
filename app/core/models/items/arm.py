from app.core.models.items.base import BaseItem
from app.crm.meta import *


class Arm(BaseItem):
    crm_parameters = {'Диаметр': 'diameter',
                      'Производитель': 'vendor', 'Тип рукава': 'arm_type'}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = ARM_PARAM_NAME
        self.category_id = ARM_CAT_ID
        self.MeasureCode = '006'
        self.MeasureName = 'Метр'
        self.MeasureInt = 'MTR'
        self.NomenclatureType = ARM_NOMENCLATURE_TYPE

    def get_selection_name(self) -> str:
        arm_type = self.parameters.get('arm_type', '')
        length = self.amount
        if length is None:
            length = ''
        diameter = self.parameters.get('diameter', '')
        return f'{arm_type}x{diameter}'
