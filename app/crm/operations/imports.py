from app.crm.models.arm import Arm
from app.crm.models.fiting import Fiting
from app.db.base import replace_upsert
from app.crm.models.clutch import Clutch
from app.crm.models.base import SiteObj
from app.db.variables import *


def import_data(tree):
    items = tree.findall("//{urn:1C.ru:commerceml_2}Товар")
    for i in items:
        req = i.find("{urn:1C.ru:commerceml_2}ЗначенияРеквизитов")
        if req is None:
            continue
        type = req[1][1].text
        obj = parse_object(i, type)


def parse_object(obj, type):
    req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
    site_obj: SiteObj
    collection = ''
    if req is None:
        return
    if type == 'Муфта':
        site_obj = Clutch.create_from_cml(obj)
        collection = clutch_collection
    elif type == 'Фитинг':
        site_obj = Fiting.create_from_cml(obj)
        collection = fiting_collection
    elif type == 'Рукав':
        site_obj = Arm.create_from_cml(obj)
        collection = arm_collection
    else:
        return

    replace_upsert(collection, {"_id": site_obj.id}, site_obj.convert_to_dict())
    return site_obj
