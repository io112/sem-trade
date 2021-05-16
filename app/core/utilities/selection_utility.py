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


def create_selection() -> RVDSelection:
    return calc_subtotal(RVDSelection())


def find_part(collection: BaseItem, query: str):
    return collection.objects.search_text(query)


def get_candidates_by_params(selection: RVDSelection):
    items = selection.items or {}
    fiting1 = items.get("fiting1", {})
    fiting2 = items.get("fiting2", {})
    clutch1 = items.get("clutch1", {})
    clutch2 = items.get("clutch2", {})
    arm = items.get("arm", {})
    clutch_params = not_zero_amount
    arms = queryset_to_list(Arm.objects().filter_params(arm))
    clutch1 = queryset_to_list(Clutch.objects().filter_params(clutch1))
    clutch2 = queryset_to_list(Clutch.objects().filter_params(clutch2))
    fiting1 = queryset_to_list(Fiting.objects().filter_params(fiting1))
    fiting2 = queryset_to_list(Fiting.objects().filter_params(fiting2))
    res = {'arm': arms, 'clutch1': clutch1, 'clutch2': clutch2,
           'fiting1': fiting1, 'fiting2': fiting2}
    return res


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


def save_selection(session: Session, items: dict, subtotal: dict) -> dict:
    selection = RVDSelection(items=items, subtotal=subtotal)
    selection = calc_subtotal(selection)
    session.selection = selection
    session.save()
    return selection.to_mongo().to_dict()


def calc_subtotal(selection: RVDSelection) -> RVDSelection:
    price = 0
    total_amount = selection.subtotal.get('amount', 1)
    if total_amount is None:
        total_amount = 1
    items = selection.items
    for i, obj in item_objects.items():
        amount = 1
        if i in items and 'id' in items[i]:
            id = items[i]['id']
            o_price = obj.objects(id=id)[0].price
            if 'amount' in items[i]:
                amount = items[i]['amount']
            price += o_price * amount
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
            amount = items[i]['amount'] if items[i].get('amount') else 1
            id = items[i]['id']
            item = obj.objects(id=id)[0]
            cart_item = CartItem(item=item, amount=amount,
                                 price=item.price, total_price=item.price * amount)
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
