import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import pytz

from app.core.utilities.order_utility import get_orders


def export_orders() -> str:
    orders = get_orders()
    res = ET.Element('КоммерческаяИнформация')
    res.attrib['xmlns'] = "urn:1C.ru:commerceml_2"
    res.attrib['xmlns:xs'] = "http://www.w3.org/2001/XMLSchema"
    res.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    res.attrib['ВерсияСхемы'] = '2.04'
    res.attrib['ДатаФормирования'] = datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime(
        "%Y-%m-%dT%H:%M:%S")

    for i in orders:
        res.append(i.create_xml_doc())

    et = ET.ElementTree(res)

    f = BytesIO()
    et.write(f, encoding='utf-8', xml_declaration=True)
    return f.getvalue().decode('UTF-8')
