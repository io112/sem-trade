from bson import ObjectId

import app.core.utilities.contragent_utility as utility
from app.core.utilities.common import *
from app.core.models.сontragent import Contragent


def get_contragent_safe_dict(contragent: Contragent) -> dict:
    contragent = document_to_dict(contragent)
    contragent['_id'] = str(contragent['_id'])
    return contragent


def get_contragent(cid: str) -> dict:
    contragent = utility.get_contragent(cid)
    return get_contragent_safe_dict(contragent)


def find_contragents(query: str):
    return utility.find_contragents(query)


def create_contragent_from_form(form_data):
    res = {}
    for i in form_data:
        i: dict
        key = i['name']
        val = i['value']
        if key == 'is_org':
            res['is_org'] = True
        else:
            res[key] = val
    utility.create_contragent(res)
