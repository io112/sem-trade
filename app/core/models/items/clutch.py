import app.db.variables as dbvars
from app.core.models.items.base import BaseItem


class Clutch(BaseItem):
    crm_parameters = {'Диаметр': 'diameter', 'Тип рукава': 'arm_type'}
    collection = dbvars.clutch_collection
    NomenclatureType = 'Муфта'

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = self.get_param_name()
        self.category_id = self.get_category_id()

    @staticmethod
    def get_param_name() -> str:
        return "clutch"

    @staticmethod
    def get_category_id() -> str:
        return "d29cf72d-6561-11ea-8182-002590a66847"

    def get_selection_name(self) -> str:
        return ''
