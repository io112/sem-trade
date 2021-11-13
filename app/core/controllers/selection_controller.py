import pytz
from mongoengine import QuerySet

import app.core.utilities.selection_utility as utility
from app.core.models.items.cart_item import CartItem
from app.core.models.selection import RVDSelection
from app.core.models.session import Session
from app.core.utilities.selection_utility import collections

msk_timezone = pytz.timezone('Europe/Moscow')

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}


def get_selection(session_id):
    session = Session.objects(id=session_id)[0]
    selection = session.selection
    if selection is None:
        selection = RVDSelection()
        return utility.update_selection(session, selection)
    return selection.get_safe()


def find_part(query, only_present, amount):
    res = {'items': []}
    search = utility.find_part(query, only_present, amount)
    for i in search:
        res['items'].append(i.get_safe())
    return res


def clear_part(session_id: str):
    session = Session.objects(id=session_id)[0]
    if session.selection and session.selection.part:
        del session.selection.part
        session.save()


def get_filtered_params(session_id, only_present):
    only_present = True if only_present == 'true' else False
    session = Session.objects(id=session_id)[0]
    if session.selection is None:
        session.selection = utility.create_selection()
        session.save()
    selection = session.selection
    candidates = utility.get_candidates_by_params(selection, only_present)
    parameters = utility.get_parameters_list(candidates)
    return {'candidates': candidates, 'parameters': parameters, 'selection': selection.get_safe()}


def get_suggestion(session_id, only_present, part_params, part_type):
    only_present = True if (only_present == 'true' or only_present is True) else False
    session = Session.objects(id=session_id)[0]
    if session.selection is None:
        session.selection = utility.create_selection()
        session.save()
    candidate = utility.get_candidate_by_params(part_params, part_type, only_present)
    parameters = utility.get_candidate_params(candidate)
    return {'suggestion': candidate, 'parameters': parameters}


def set_part(session_id: str, collection: str, part_id: str, amount: float):
    if amount == '':
        amount = 0
    session = Session.objects(id=session_id)[0]
    collection = collections[collection]
    part = collection.objects(id=part_id)[0]
    price = round(part.price * utility.get_price_coef(part.price, amount), 2)
    item = CartItem(name=part.name, item=part, amount=amount, price=price, total_price=round(price * amount, 2))
    selection = utility.save_selection(session, [], {}, item)
    res_part = selection['part']
    res = {'current_part': res_part}
    return res


def update_selection(session_id: str, selection: dict):
    session: QuerySet = Session.objects(id=session_id)
    session: Session = session[0]
    if selection['items'] is not None:
        selection['items'] = set_linked_params(selection['items'])
    return utility.save_selection(session, selection['items'], selection['subtotal'])


def add_item_to_selection(session_id: str, part: dict, job_type: str):
    session: QuerySet = Session.objects(id=session_id)
    session: Session = session[0]
    selection = session.selection
    if selection is None:
        selection = RVDSelection()
    selection.items.append(utility.get_cart_item(job_type, part))
    return utility.update_selection(session, selection)


def del_item_from_selection(session_id: str, item_index: int):
    session: QuerySet = Session.objects(id=session_id)
    session: Session = session[0]
    selection = session.selection
    if selection is None:
        selection = RVDSelection()
    if item_index >= len(selection.items):
        return selection.get_safe()
    del selection.items[item_index]
    return utility.update_selection(session, selection)


def set_job_type(session_id: str, type: str):
    session: QuerySet = Session.objects(id=session_id)
    session: Session = session[0]
    selection = session.selection
    selection.subtotal['job_type'] = type
    return utility.update_selection(session, selection)


def update_amount(session_id: str, amount: float):
    session: QuerySet = Session.objects(id=session_id)
    session: Session = session[0]
    selection = session.selection
    selection.subtotal['amount'] = amount
    return utility.update_selection(session, selection)


def cart_item_from_part(part: dict, amount: float):
    return utility.get_cart_item_from_part(part, amount)


def set_linked_params(items: dict) -> dict:
    DN = None
    for item in items.values():
        if item['type'] == 'arm':
            DN = item.get('diameter')
            break
    for item in items.values():
        if item['type'] == 'clutch' or item['type'] == 'fiting':
            if DN is not None:
                item['diameter'] = DN
            elif item.get('diameter'):
                del item['diameter']
    return items
