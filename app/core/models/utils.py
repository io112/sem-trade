from app.core.models.items.arm import Arm
from app.core.models.items.base import BaseItem
from app.core.models.items.clutch import Clutch
from app.core.models.items.empty_item import EmptyItem
from app.core.models.items.fiting import Fiting
from app.core.models.items.pipe import Pipe
from app.crm.meta import *

objects = {ARM_PARAM_NAME: Arm, CLUTCH_PARAM_NAME: Clutch,
           FITING_PARAM_NAME: Fiting, PIPE_PARAM_NAME: Pipe}


def create_simple_item(name: str, out_name: str) -> BaseItem:
    if name is None:
        name = ""
    for i in objects:
        if i == name:
            return objects[i](out_name)
    return EmptyItem()


def create_item(item_type: str, out_name: str) -> BaseItem:
    from app.core.models.items.composite_item import CompositeItem
    if item_type is None:
        item_type = ""
    if item_type == CompositeItem.get_param_name():
        return CompositeItem(out_name)
    for i in objects:
        if i == item_type:
            return objects[i](out_name)
    return EmptyItem()
