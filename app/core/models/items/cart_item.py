from mongoengine import EmbeddedDocument, GenericReferenceField, FloatField

from app.core.utilities.common import document_to_dict
import xml.etree.ElementTree as ET


class CartItem(EmbeddedDocument):
    item = GenericReferenceField()
    amount = FloatField()
    price = FloatField()
    total_price = FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_safe(self) -> dict:
        res = document_to_dict(self)
        res['item'] = self.item.get_safe()
        return res

    def create_xml(self, amount=None) -> list:
        amount = amount if amount is not None else self.amount
        item = self.item
        res = ET.Element('Товар')
        ET.SubElement(res, 'Ид').text = str(item.id)
        ET.SubElement(res, 'Наименование').text = item.NomenclatureType
        measure = ET.Element('БазоваяЕдиница')
        measure.text = item.MeasureText
        measure.attrib['Код'] = item.MeasureCode
        measure.attrib['НаименованиеПолное'] = item.MeasureName
        measure.attrib['МеждународноеСокращение'] = item.MeasureInt
        res.append(measure)
        ET.SubElement(res, 'ЦенаЗаЕдиницу').text = str(self.price)
        ET.SubElement(res, 'Количество').text = str(amount)
        ET.SubElement(res, 'Сумма').text = str(self.price * amount)
        recs = ET.Element('ЗначенияРеквизитов')
        rec1 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec1, 'Наименование').text = 'ВидНоменклатуры'
        ET.SubElement(rec1, 'Значение').text = item.NomenclatureType
        rec2 = ET.Element('ЗначениеРеквизита')
        ET.SubElement(rec2, 'Наименование').text = 'ТипНоменклатуры'
        ET.SubElement(rec2, 'Значение').text = 'Товар'
        recs.append(rec1)
        recs.append(rec2)
        res.append(recs)

        return [res]
