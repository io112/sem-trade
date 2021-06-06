import app.db.variables as dbvars
from app.core.models.items.base import BaseItem


class Fiting(BaseItem):
    crm_parameters = {'Тип фиттинга': 'fiting_type', 'Диаметр': 'diameter',
                      'Угол': 'angle', 'Резьба': 'carving'}
    NomenclatureType = 'Фитинг'

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = self.get_param_name()
        self.category_id = self.get_category_id()

    @staticmethod
    def get_param_name() -> str:
        return "fiting"

    @staticmethod
    def get_category_id() -> str:
        return "612c1a12-6567-11ea-8182-002590a66847"

    def get_selection_name(self) -> str:
        type = self.parameters.get('fiting_type', '')
        carving = self.parameters.get('carving', '')
        return f'({type} {carving})'
