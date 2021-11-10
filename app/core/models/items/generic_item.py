from app.core.models.items.base import BaseItem


class GenericItem(BaseItem):
    crm_parameters = {'Размер': 'size'}
    MeasureCode = '006'
    MeasureName = 'Метр'
    MeasureInt = 'MTR'
    MeasureText = 'метров'
    NomenclatureType = 'Трубка'

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = self.get_param_name()
        self.category_id = self.get_category_id()

    @staticmethod
    def get_param_name() -> str:
        return "pipe"

    @staticmethod
    def get_category_id() -> str:
        return 'd6d02938-c6ee-11eb-9258-00155d462101'

    def get_selection_name(self) -> str:
        return f''
