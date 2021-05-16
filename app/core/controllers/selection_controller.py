from copy import deepcopy

import pytz
from mongoengine import QuerySet

from app.core.models.selection import RVDSelection
from app.core.session_vault import *
import app.core.utilities.selection_utility as utility
from datetime import datetime

from app.core.utilities.selection_utility import collections

msk_timezone = pytz.timezone('Europe/Moscow')

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}


def get_selection(session_id):
    session = Session.objects(id=session_id)[0]
    selection = session.selection
    if selection is None:
        return 'NaN'
    return selection.to_mongo().to_dict()


def find_part(collection, query):
    res = []
    collection_object = None
    for i in collections:
        if i == collection:
            collection_object = collections[i]
    if collection_object is not None:
        search = utility.find_part(collection_object, query)
        for i in search:
            res.append(i.get_safe())
        return res
    else:
        return []


def get_filtered_params(session_id, ignore_amounts=False):
    session = Session.objects(id=session_id)[0]
    if session.selection is None:
        session.selection = utility.create_selection()
        session.save()
    selection = session.selection
    candidates = utility.get_candidates_by_params(selection)
    parameters = utility.get_parameters_list(candidates)
    return {'candidates': candidates, 'parameters': parameters, 'selection': selection.to_mongo().to_dict()}


def update_selection(session_id: str, selection: dict):
    session: QuerySet = Session.objects(id=session_id)
    session: Session = session[0]
    return utility.save_selection(session, selection['items'], selection['subtotal'])
