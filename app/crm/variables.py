from app.core.models.items.arm import Arm
from app.core.models.items.clutch import Clutch
from app.core.models.items.fiting import Fiting
from app.core.models.items.pipe import Pipe

available_types = [Arm, Clutch, Fiting, Pipe]
category_ids = {}
nomenclatyre_types = {}
for i in available_types:
    category_ids[i.get_category_id()] = i
    nomenclatyre_types[i.NomenclatureType] = i
