from app.core.models.items.arm import Arm
from app.core.models.items.clutch import Clutch
from app.core.models.items.fiting import Fiting
from app.core.models.items.pipe import Pipe

collections = {'arm': Arm, 'clutch': Clutch, 'fiting': Fiting, 'pipe': Pipe}


def get_item(type, id):
    obj = collections.get(type)
    if obj is not None:
        item = obj.objects(id=id)[0]
        return item
    return None
