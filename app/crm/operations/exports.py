import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import pytz

from app.utilities.orders_controller import get_all_orders


def export_orders() -> str:
    orders = get_all_orders()
    res = ET.Element('КоммерческаяИнформация')
    res.attrib['xmlns'] = "urn:1C.ru:commerceml_2"
    res.attrib['xmlns:xs'] = "http://www.w3.org/2001/XMLSchema"
    res.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    res.attrib['ВерсияСхемы'] = '2.07'
    res.attrib['ДатаФормирования'] = datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime(
            "%Y-%m-%dT%H:%M:%S")

    for i in orders:
        res.append(i.create_xml_doc())

    et = ET.ElementTree(res)

    f = BytesIO()
    et.write(f, encoding='utf-8', xml_declaration=True)
    print(f.getvalue().decode('UTF-8'))
    return ET.tostring(res, encoding='UTF-8').decode('UTF-8')
