from app.db.base import replace_upsert
from app.crm.models.clutch import Clutch


def import_data(tree):
    items = tree.findall("//{urn:1C.ru:commerceml_2}Товар")
    for i in items:
        req = i.find("{urn:1C.ru:commerceml_2}ЗначенияРеквизитов")
        if req is None:
            continue
        type = req[1][1].text
        obj = parse_objects(i, type)
        print(obj)


def parse_objects(obj, type):
    req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
    if req is None:
        return
    if type == 'Муфта':
        clutch = Clutch(obj[0].text, obj[2].text, obj[3].attrib['НаименованиеПолное'],
                        req[1][2].text, req[0][2].text, req[2][2].text)
        replace_upsert('clutch', {"_id": clutch.id}, clutch.convert_to_dict())
        return clutch
