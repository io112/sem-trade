from typing import Dict, List

from app.core.controllers.price_controller import RVDPrice, PartPrice
from app.core.models.items.arm import Arm
from app.core.models.items.base import BaseItem
from app.core.models.items.cart_item import CartItem
from app.core.models.items.fiting import Fiting
from app.core.models.selection import RVDSelection
from app.core.models.session import Session
from app.core.utilities.common import queryset_to_list
from app.core.utilities.items_utility import collections

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}

price_coefficients = {'hydro': 1, 'gur': 1, 'break': 1, 'conditioner': 1, 'clutch': 1, 'transmission': 1}


def create_selection() -> RVDSelection:
    return calc_subtotal(RVDSelection())


def find_part(query: str, only_present, amount: int = 0):
    collection = BaseItem
    if amount == '':
        amount = 0
    querymod = {'name__icontains': query}
    if only_present:
        querymod['amount__gt'] = 0

    res = collection.objects(**querymod)
    for i in res:
        price_coefficient = get_price_coef(i.price, float(amount))
        i.price = round(i.price * price_coefficient, 2)
    return res


def get_candidates_by_params(selection: RVDSelection, only_present):
    items = selection.items or {}
    res = {}
    for key, value in items.items():
        t = value.get('type')
        if t is None:
            continue
        type_item = collections.get(t)
        if type_item is not None:
            res[key] = queryset_to_list(__get_filtered_item(type_item, only_present, value))
    return res


def get_candidate_by_params(params: dict, type: str, only_present):
    type_item = collections.get(type)
    if type_item is not None:
        res = queryset_to_list(__get_filtered_item(type_item, only_present, params))
    else:
        return None
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
        get_candidate_params(value)
    return res


def get_candidate_params(candidate) -> dict:
    if type(candidate) == dict:
        return get_parameters_list(candidate)
    return get_available_parameters(candidate)


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
    for i in res:
        try:
            res[i].sort()
        except:
            pass
    return res


def save_selection(session: Session, items: list, subtotal: dict, part: CartItem = None) -> dict:
    selection = RVDSelection(items=items, subtotal=subtotal, part=part)
    selection = calc_subtotal(selection)
    selection = copy_selection_parameters(selection)
    session.selection = selection
    session.save()
    return selection.get_safe()


def update_selection(session: Session, selection: RVDSelection) -> dict:
    session.selection = calc_subtotal(selection)
    session.save()
    return selection.get_safe()


def copy_selection_parameters(selection: RVDSelection) -> RVDSelection:
    selected_items = get_selected_items(selection)
    if len(selected_items) > 0:
        for key, item in selected_items.items():
            if item.item:
                for k, v in item.item.parameters.items():
                    selection['items'][key][k] = v
    selection['items'] = fix_linked_params(selection['items'])
    return selection


def fix_linked_params(items: Dict[str, dict]) -> Dict[str, dict]:
    DN = None
    for item in items.values():
        if item['type'] == 'arm':
            DN = item.get('diameter')
            break
    for i in items:
        item = items[i]
        if item['type'] == 'clutch' or item['type'] == 'fiting':
            cur_dn = item.get('diameter')
            if DN is not None and cur_dn is not None and DN != cur_dn:
                items[i] = {'type': item.get('type', ''), 'part_name': item.get('part_name', '')}
            elif DN is None and cur_dn is not None:
                del items[i]['diameter']
            if DN is not None:
                items[i]['diameter'] = DN
    return items


def calc_subtotal(selection: RVDSelection) -> RVDSelection:
    price = 0
    total_amount = selection.subtotal.get('amount', 1)
    selected_items = selection.items
    for obj in selection.items:
        p = RVDPrice.calc_cart_item_price(obj, selection.subtotal['job_type'])
        obj.price = p.price
        obj.total_price = p.full_price
        price += obj.total_price
    selection.subtotal['price'] = RVDPrice.round_price(price)
    selection.subtotal['total_price'] = RVDPrice.round_price(price * total_amount)
    selection.subtotal['name'] = create_selection_name(selected_items)
    selection.subtotal['amount'] = total_amount
    return selection


def get_selected_items(selection: RVDSelection) -> Dict[str, CartItem]:
    res = {}
    services_price = get_services_price(selection)
    fp = get_full_price(selection)
    price_coef = get_price_coef(fp['total_price'])
    items_amount = services_price['items_amount']
    services_price = services_price['services_price']
    additional_price = round(services_price / items_amount, 2) if items_amount else 0
    price_coefficient = price_coefficients.get(selection.subtotal.get('job_type'), 1)
    if not (selection and selection.items):
        return {}
    items = selection.items
    for key, value in items.items():
        obj = collections.get(value['type'])
        if obj is not None and 'id' in value:
            amount = value['amount'] if value.get('amount') is not None else 1
            id = value['id']
            item = obj.objects(id=id)[0]
            price = item.price * price_coefficient
            price += price * price_coef + additional_price
            price = round(price, 2)
            total_price = round(price * amount, 2)
            cart_item = CartItem(name=item.name, local_name=value.get('part_name', ''), item=item, amount=amount,
                                 price=price, total_price=total_price)
            res[key] = cart_item
        if value['type'] == 'service':
            cart_item = CartItem(name=value.get('part_name', ''), amount=1,
                                 price=0, total_price=0)
            res[key] = cart_item
    return res


def get_cart_item(rvd_type: str, part: dict):
    if part['type'] == 'service':
        return CartItem(name=part['name'], local_name='', amount=1,
                        price=part['price'], total_price=part['price'])
    obj = collections.get(part['type'])
    item = obj.objects(id=part['id'])[0]
    amount = part['amount']
    price = RVDPrice.calc_part_price(part, rvd_type)
    cart_item = CartItem(name=item.name, local_name='', item=item, amount=amount,
                         price=price.price, total_price=price.full_price)
    return cart_item


def get_cart_item_from_part(part: dict, amount: float):
    if part['type'] == 'service':
        return CartItem(name=part['name'], local_name='', amount=1,
                        price=amount, total_price=amount)
    obj = BaseItem
    item = obj.objects(id=part['_id'])[0]
    price = PartPrice.calc_part_price(part, amount)
    cart_item = CartItem(name=item.name, local_name='', item=item, amount=amount,
                         price=price.price, total_price=price.full_price)
    return cart_item


def get_price_coef(price, amount=1.0):
    total_price = price * amount
    if total_price <= 100:
        return 3
    elif total_price <= 500:
        return 1.3
    elif total_price <= 1000:
        return 0.8
    else:
        return 0.5


def get_services_price(selection: RVDSelection) -> Dict[str, float]:
    res = {'items_amount': 0, 'services_price': 0}
    price = 0
    total_items_amount = 0
    total_amount = selection.subtotal.get('amount', 1)
    if not (selection and selection.items):
        return res
    items = selection.items
    for key, value in items.items():
        if value['type'] == 'service':
            price += float(value.get('amount', 0))
        elif 'id' in value:
            total_items_amount += value.get('amount', 0)
    return {'items_amount': total_items_amount * total_amount, 'services_price': price}


def get_full_price(selection: RVDSelection) -> Dict[str, float]:
    res = {'items_amount': 0, 'total_price': 0}
    price = 0
    total_items_amount = 0
    total_amount = selection.subtotal.get('amount', 1)
    if not (selection and selection.items):
        return res
    items = selection.items
    for key, value in items.items():
        obj = collections.get(value['type'])
        if obj is not None and 'id' in value:
            item = obj.objects(id=value['id'])[0]
            price += item.price * value.get('amount', 0)
            total_items_amount += value.get('amount', 0)
    return {'items_amount': total_items_amount * total_amount, 'total_price': price}


def create_selection_name(items: List[CartItem]):
    arms = ''
    fitings = ''
    for i in items:
        item = i.item
        if type(item) == Arm:
            arms += (' ' if arms != '' else '') + str(i.amount) + ' м.' + ' ' + item.get_selection_name()
        if type(item) == Fiting:
            fitings += ('+' if fitings != '' else '') + item.get_selection_name()
    return f'Рукав {arms} {fitings}'
