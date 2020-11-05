from app.crm.models.arm import Arm
from app.crm.variables import *
from app.crm.models.fiting import Fiting
from app.crm.models.offer import Offer
from app.db.base import update_upsert, replace_upsert
from app.crm.models.clutch import Clutch
from app.crm.models.base import SiteObj
from app.db.variables import *


def import_data(tree):
    if not tree.getroot().find('{urn:1C.ru:commerceml_2}Предложения') is None:
        import_offers(tree)
    elif not tree.findall('{urn:1C.ru:commerceml_2}Каталог') is None:
        import_objects(tree)


def import_objects(tree):
    items = tree.findall("//{urn:1C.ru:commerceml_2}Товар")
    for i in items:
        req = i.find("{urn:1C.ru:commerceml_2}ЗначенияРеквизитов")
        if req is None:
            continue
        type = req[1][1].text
        obj = parse_object(i, type)


def import_offers(tree):
    items = tree.findall("//{urn:1C.ru:commerceml_2}Предложение")
    for i in items:
        req = i.find("{urn:1C.ru:commerceml_2}ИдХарактеристики")
        if req is None:
            continue
        obj = parse_offer(i)


def parse_offer(obj):
    offer = Offer.create_from_cml(obj)
    collection = ''
    if offer.id == clutch_cat_id:
        collection = clutch_collection
    elif offer.id == arm_cat_id:
        collection = arm_collection
    elif offer.id == fiting_cat_id:
        collection = fiting_collection

    return offer


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
