from copy import deepcopy

import pytz
from mongoengine import QuerySet

from app.core.models.selection import RVDSelection
from app.core.session_vault import *
import app.core.utilities.selection_utility as utility
from datetime import datetime

from app.core.utilities import session_utility, contragent_utility

msk_timezone = pytz.timezone('Europe/Moscow')

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}


def get_selection(session_id):
    session = Session.objects(id=session_id)[0]
    selection = session.selection
    if selection is None:
        return 'NaN'
    return selection.to_mongo().to_dict()


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


