import pytz
from mongoengine import QuerySet

import app.core.utilities.selection_utility as utility
from app.core.models.items.cart_item import CartItem
from app.core.models.session import Session
from app.core.utilities.selection_utility import collections

msk_timezone = pytz.timezone('Europe/Moscow')

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}


def get_selection(session_id):
    session = Session.objects(id=session_id)[0]
    selection = session.selection
    if selection is None:
        return 'NaN'
    return selection.to_mongo().to_dict()


def find_part(collection, query, only_present):
    res = {'items': []}
    collection_object = None
    for i in collections:
        if i == collection:
            collection_object = collections[i]
    if collection_object is not None:
        search = utility.find_part(collection_object, query, only_present)
        for i in search:
            res['items'].append(i.get_safe())
        return res
    else:
        return {}


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


def set_part(session_id: str, collection: str, part_id: str, amount: float):
    if amount == '':
        amount = 0
    session = Session.objects(id=session_id)[0]
    collection = collections[collection]
    part = collection.objects(id=part_id)[0]
    price = round(part.price * utility.price_coefficient, 2)
    item = CartItem(name=part.name, item=part, amount=amount, price=price, total_price=round(price * amount, 2))
    selection = utility.save_selection(session, {}, {}, item)
    res_part = selection['part']
    res = {'current_part': res_part}
    return res


def update_selection(session_id: str, selection: dict):
    session: QuerySet = Session.objects(id=session_id)
    session: Session = session[0]
    return utility.save_selection(session, selection['items'], selection['subtotal'])
