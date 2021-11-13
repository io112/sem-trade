from app.core.models.items.generic_item import GenericItem
from app.crm.variables import category_ids, nomenclature_types


def import_data(tree):
    if not tree.getroot().find('{urn:1C.ru:commerceml_2}ПакетПредложений') is None:
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
        parse_object(i, type)


def import_offers(tree):
    items = tree.findall("//{urn:1C.ru:commerceml_2}Предложение")
    for i in items:
        req = i.find("{urn:1C.ru:commerceml_2}БазоваяЕдиница")
        if req is None:
            continue
        parse_offer(i)


def parse_offer(obj):
    id = obj[0].text
    collection_id = id[:36]
    if collection_id in category_ids.keys():
        item = category_ids[collection_id]
    else:
        item = GenericItem
    item = item.objects(id=id).first()
    if item is None:
        return
    item.price = float(obj.find("{urn:1C.ru:commerceml_2}Цены")[0][2].text)
    item.amount = float(obj.find("{urn:1C.ru:commerceml_2}Количество").text)
    item.save()


def parse_object(obj, type):
    # req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
    if type in nomenclature_types.keys():
        create_object(obj, nomenclature_types[type], type)
    else:
        create_object(obj, GenericItem, type)


def create_object(obj, obj_type, nomeclature_type):
    res = obj_type()
    res.id = obj[0].text
    if obj_type == GenericItem:
        res.NomenclatureType = nomeclature_type
        res.type = nomeclature_type
        res.category_id = res.id[:res.id.find('#')]
    res.name = obj[2].text
    res.MeasureCode = obj[3].attrib['Код'].strip()
    res.measure = obj[3].attrib['НаименованиеПолное']
    res.MeasureInt = obj[3].attrib['МеждународноеСокращение']
    res.MeasureName = obj[3].attrib['НаименованиеПолное']

    req = obj.find("{urn:1C.ru:commerceml_2}ХарактеристикиТовара")
    if req is not None:
        for i in req:
            param = i[2].text
            try:
                param = float(i[2].text)
            except:
                pass
            if i[1].text in obj_type.crm_parameters.keys():
                res.parameters[obj_type.crm_parameters[i[1].text]] = param
            else:
                res.parameters[i[1].text] = param

    res.save()
