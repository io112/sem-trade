from app.core.models.items.arm import Arm
from app.core.models.items.clutch import Clutch
from app.core.models.items.fiting import Fiting
from app.core.models.items.pipe import Pipe
from app.crm.meta import *

available_types = [Arm, Clutch, Fiting, Pipe]
category_ids = {ARM_CAT_ID: Arm, CLUTCH_CAT_ID: Clutch,
                FITING_CAT_ID: Fiting, PIPE_CAT_ID: Pipe}
nomenclature_types = {ARM_NOMENCLATURE_TYPE: Arm, CLUTCH_NOMENCLATURE_TYPE: Clutch,
                      FITING_NOMENCLATURE_TYPE: Fiting, PIPE_NOMENCLATURE_TYPE: Pipe}
