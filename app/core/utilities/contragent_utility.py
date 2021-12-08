from bson import ObjectId

from app.core.models.сontragent import Contragent
from app.core.utilities.common import *


def get_contragent(cid: str):
    contragent = Contragent.objects(id=ObjectId(cid))[0]
    return contragent


def find_contragents(query: str):
    querymod = {'name__icontains': query}

    contragent = Contragent.objects(**querymod)
    contr_list = queryset_to_list(contragent)
    for i in range(len(contr_list)):
        contr_list[i]['_id'] = str(contr_list[i]['_id'])
    return contr_list


def create_contragent(data: dict):
    Contragent(**data).save()
