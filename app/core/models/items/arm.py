from app.core.models.items.base import BaseItem


class Arm(BaseItem):
    crm_parameters = {'Диаметр': 'diameter',
                      'Производитель': 'vendor', 'Тип рукава': 'arm_type'}
    MeasureCode = '006'
    MeasureName = 'Метр'
    MeasureInt = 'MTR'
    MeasureText = 'метров'
    NomenclatureType = 'Рукав'

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = self.get_param_name()
        self.category_id = self.get_category_id()

    @staticmethod
    def get_param_name() -> str:
        return "arm"

    @staticmethod
    def get_category_id() -> str:
        return "d9da1352-656c-11ea-8182-002590a66847"

    def get_selection_name(self) -> str:
        arm_type = self.parameters.get('arm_type', '')
        length = self.amount
        if length is None:
            length = ''
        diameter = self.parameters.get('diameter', '')
        return f'{arm_type}x{diameter}'
