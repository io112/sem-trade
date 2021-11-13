from app.core.models.items.base import BaseItem
from app.crm.meta import FITING_NOMENCLATURE_TYPE, FITING_CAT_ID, FITING_PARAM_NAME


class Fiting(BaseItem):
    crm_parameters = {'Тип фиттинга': 'fiting_type', 'Диаметр': 'diameter',
                      'Угол': 'angle', 'Резьба': 'carving'}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.type = FITING_PARAM_NAME
        self.category_id = FITING_CAT_ID
        self.NomenclatureType = FITING_NOMENCLATURE_TYPE

    def get_selection_name(self) -> str:
        type = self.parameters.get('fiting_type', '')
        carving = self.parameters.get('carving', '')
        return f'({type} {carving})'
