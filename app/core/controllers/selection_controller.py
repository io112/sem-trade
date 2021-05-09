from copy import deepcopy

import pytz
from mongoengine import QuerySet

from app.core.models.selection import RVDSelection
from app.core.session_vault import *
import app.core.utilities.selection_utility as utility
from datetime import datetime

msk_timezone = pytz.timezone('Europe/Moscow')

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}


def get_filtered_params(session_id, ignore_amounts=False):
    session = Session.objects(id=session_id)[0]
    selection = session.selection
    candidates = utility.get_candidates_by_params(selection)
    print(candidates)


def update_selection(session: QuerySet, selection: dict):
    session: Session = session[0]
    items = deepcopy(selection)
    if items['subtotal']:
        del items['subtotal']
    selection = RVDSelection(items=items, subtotal=selection['subtotal'])
    session.selection = selection
    session.save()
