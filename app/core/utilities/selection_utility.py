from typing import Dict

from app.core.models.items.arm import Arm
from app.core.models.items.base import BaseItem
from app.core.models.items.cart_item import CartItem
from app.core.models.items.clutch import Clutch
from app.core.models.items.fiting import Fiting
from app.core.models.selection import RVDSelection
from app.core.models.session import Session
from app.core.utilities.common import queryset_to_list

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}
item_objects = {'arm': Arm, 'clutch1': Clutch, 'clutch2': Clutch,
                'fiting1': Fiting, 'fiting2': Fiting}
collections = {'arm': Arm, 'clutch': Clutch, 'fiting': Fiting}
price_coefficient = 2.2


def create_selection() -> RVDSelection:
    return calc_subtotal(RVDSelection())


def find_part(collection: BaseItem, query: str, only_present):
    if only_present:
        res = collection.objects(amount__gt=0)
    else:
        res = collection.objects
    res = res.search_text(query)
    for i in res:
        i.price = round(i.price * price_coefficient, 2)
    return res


def get_candidates_by_params(selection: RVDSelection, only_present):
    items = selection.items or {}
    present_filter = {'amount__gt': 0} if only_present else None
    fiting1 = items.get("fiting1", {})
    fiting2 = items.get("fiting2", {})
    clutch1 = items.get("clutch1", {})
    clutch2 = items.get("clutch2", {})
    arm = items.get("arm", {})
    arms = queryset_to_list(__get_filtered_item(Arm, only_present, arm))
    clutch1 = queryset_to_list(__get_filtered_item(Clutch, only_present, clutch1))
    clutch2 = queryset_to_list(__get_filtered_item(Clutch, only_present, clutch2))
    fiting1 = queryset_to_list(__get_filtered_item(Fiting, only_present, fiting1))
    fiting2 = queryset_to_list(__get_filtered_item(Fiting, only_present, fiting2))
    res = {'arm': arms, 'clutch1': clutch1, 'clutch2': clutch2,
           'fiting1': fiting1, 'fiting2': fiting2}
    return res


def __get_filtered_item(item, only_present, params):
    if only_present:
        res = item.objects(amount__gt=0)
    else:
        res = item.objects
    return res.filter_params(params)


def get_parameters_list(all_candidates: dict) -> dict:
    res = {}
    for key, value in all_candidates.items():
        if type(value) == dict:
            res[key] = get_parameters_list(value)
            continue
        res[key] = get_available_parameters(value)
    return res


def get_available_parameters(candidates: list) -> dict:
    res = {}
    for i in candidates:
        params: dict = i['parameters']
        for key, value in params.items():
            if key not in res:
                res[key] = [value]
                continue
            if value not in res[key]:
                res[key].append(value)
    return res


def save_selection(session: Session, items: dict, subtotal: dict, part: CartItem = None) -> dict:
    selection = RVDSelection(items=items, subtotal=subtotal, part=part)
    selection = calc_subtotal(selection)
    session.selection = selection
    session.save()
    return selection.get_safe()


def calc_subtotal(selection: RVDSelection) -> RVDSelection:
    price = 0
    total_amount = selection.subtotal.get('amount', 1)
    if total_amount is None:
        total_amount = 1
    items = selection.items
    for _, obj in get_selected_items(selection).items():
        price += obj.total_price
    selection.subtotal['price'] = price
    selection.subtotal['total_price'] = price * total_amount
    selection.subtotal['name'] = create_selection_name(items)
    selection.subtotal['amount'] = total_amount
    return selection


def get_selected_items(selection: RVDSelection) -> Dict[str, CartItem]:
    res = {}
    if not (selection and selection.items):
        return {}
    items = selection.items
    for i, obj in item_objects.items():
        if i in items and 'id' in items[i]:
            amount = items[i]['amount'] if items[i].get('amount') is not None else 1
            id = items[i]['id']
            item = obj.objects(id=id)[0]
            price = round(item.price * price_coefficient, 2)
            cart_item = CartItem(name=item.name, item=item, amount=amount,
                                 price=price, total_price=round(price * amount, 2))
            res[i] = cart_item
    return res


def create_selection_name(items: dict):
    arm = items.get('arm', {})
    fit1 = items.get('fiting1', {})
    fit2 = items.get('fiting2', {})
    arm_type = arm.get('arm_type', '')
    diameter = arm.get('diameter', '')
    braid = arm.get('braid', '')
    fit1_d = fit1.get('diameter', '')
    fit2_d = fit2.get('diameter', '')
    fit1_type = fit1.get('fiting_type', '')
    fit2_type = fit2.get('fiting_type', '')
    fit1_carving = fit1.get('carving', '')
    fit2_carving = fit2.get('carving', '')
    return f'Рукав {arm_type}x{diameter} {braid} ' \
           f'({fit1_type} d:{fit1_d} {fit1_carving})+' \
           f'({fit2_type} d:{fit2_d} {fit2_carving})'
