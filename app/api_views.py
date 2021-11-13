import json
import sys
import traceback

import pytz
from flask import request, jsonify, make_response, abort, Response
from flask_login import login_required, current_user

from app import app
from app.core.controllers import order_controller, selection_controller, session_controller, contragent_controller, \
    users_controller, price_controller
from app.misc import sid_required, check_sid

# ----------------SESSION ENDPOINTS---------------

msk_timezone = pytz.timezone('Europe/Moscow')


@app.route('/api/sessions/remove_session', methods=['POST'])
@login_required
def route_remove_session():
    sid = json.loads(request.form.get('data'))
    if sid is None:
        abort(404, 'sid not found')
    if not check_sid(sid):
        abort(404, 'session not found')
    session_controller.remove_session(sid)
    sessions = session_controller.get_user_sessions(current_user.username)
    sessions = sessions
    resp = make_response(jsonify(sessions))
    current_order = request.cookies.get('current_order')
    if current_order is not None and current_order == sid:
        if len(sessions) == 0:
            resp.delete_cookie('current_order')
        else:
            resp.set_cookie('current_order', sessions['data'][0]['_id'])
    return resp


@app.route('/api/sessions/get_sessions', methods=['POST'])
@login_required
def get_sessions():
    d = json.loads(request.data)
    limit = int(d.get('limit', 0))
    offset = int(d.get('offset', 0))
    sessions = session_controller.get_user_sessions(current_user.username, limit=limit, offset=offset)
    return jsonify(sessions)


@app.route('/api/orders/get_orders', methods=['POST'])
@login_required
def get_orders():
    d = json.loads(request.data)
    limit = int(d.get('limit', 0))
    offset = int(d.get('offset', 0))
    orders = order_controller.get_all_orders(limit=limit, offset=offset)
    return jsonify(orders)


@app.route('/api/orders/get_order', methods=['POST'])
@login_required
def get_order():
    order_id = json.loads(request.form.get('data'))
    order = order_controller.get_order(order_id)
    return jsonify(order)


@app.route('/api/orders/<string:order_id>/set_upd', methods=['POST'])
@login_required
def set_upd(order_id):
    upd = json.loads(request.form.get('data'))
    order = order_controller.set_upd(order_id, upd)
    return jsonify(order)


@app.route('/api/orders/<string:order_id>/download_upd', methods=['POST'])
@login_required
def download_upd(order_id):
    return order_controller.get_upd(order_id)


@app.route('/api/orders/<string:order_id>/download_bill', methods=['POST'])
@login_required
def download_bill(order_id):
    return order_controller.get_bill(order_id)


@app.route('/api/orders/<string:order_id>/close', methods=['POST'])
@login_required
def close_order(order_id):
    try:
        order = order_controller.close_order(order_id)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=409)
    return jsonify(order)


@app.route('/api/orders/<string:order_id>/checkout', methods=['POST'])
@login_required
def checkout_order(order_id):
    try:
        order = order_controller.checkout_order(order_id)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=409)
    return jsonify(order)


# ----------------CREATE ORDER ENDPOINTS------------


@app.route('/api/make_order/update_selection_items', methods=['POST'])
@login_required
@sid_required
def update_session_view():
    sid = request.cookies.get('current_order')
    data = json.loads(request.form.get('data', {}))
    return selection_controller.update_selection(sid, data)


@app.route('/api/make_order/add_item_to_selection', methods=['POST'])
@login_required
@sid_required
def update_selection_items():
    sid = request.cookies.get('current_order')
    data = json.loads(request.data)
    return jsonify(selection_controller.add_item_to_selection(sid, data['part'], data['type']))


@app.route('/api/make_order/find_part', methods=['POST'])
@login_required
@sid_required
def find_part():
    data = json.loads(request.data)
    res = selection_controller.find_part(data['query'], data.get('only_present'),
                                         data.get('amount', 1))
    return jsonify(res)


@app.route('/api/make_order/clear_part', methods=['POST'])
@login_required
@sid_required
def clear_part():
    sid = request.cookies.get('current_order')
    selection_controller.clear_part(sid)
    return jsonify('success')


@app.route('/api/make_order/cancel', methods=['POST'])
@login_required
@sid_required
def remove_order():
    sid = request.cookies.get('current_order')
    session_controller.remove_session(sid)
    sessions = session_controller.get_user_sessions(current_user.username)
    sessions = sessions['data']
    if len(sessions) > 0:
        return jsonify(sessions[0]['_id'])
    else:
        resp = make_response(jsonify(''))
        resp.delete_cookie('current_order')
        return resp


@app.route('/api/make_order/remove_contragent', methods=['POST'])
@login_required
@sid_required
def remove_contragent():
    sid = request.cookies.get('current_order')
    session_controller.del_contragent(sid)
    return jsonify({})


@app.route('/api/make_order/set_contragent', methods=['POST'])
@login_required
@sid_required
def set_contragent():
    sid = request.cookies.get('current_order')
    contragent_id = json.loads(request.data)['id']
    try:
        session_controller.set_contragent(sid, contragent_id)
        return contragent_controller.get_contragent(contragent_id)
    except Exception as e:
        traceback.print_exc()
        return str(sys.exc_info()[0]), 404


@app.route('/api/make_order/get_contragent', methods=['POST'])
@sid_required
@login_required
def get_contragent():
    sid = request.cookies.get('current_order')
    try:
        contragent = session_controller.get_contragent(sid)
        return contragent
    except Exception as e:
        traceback.print_exc()
        return jsonify({})


# ----------------SELECTION ENDPOINTS---------------

@app.route('/api/make_order/update_selection', methods=['POST'])
@sid_required
@login_required
def update_select():
    sid = request.cookies.get('current_order')
    return jsonify(selection_controller.get_selection(sid))


@app.route('/api/make_order/set_part', methods=['POST'])
@sid_required
@login_required
def set_part():
    sid = request.cookies.get('current_order')
    data = json.loads(request.form.get('data'))
    collection = data['collection']
    part_id = data['part_id']
    amount = data['amount']
    return selection_controller.set_part(sid, collection, part_id, amount)


@app.route('/api/make_order/submit_part', methods=['POST'])
@sid_required
@login_required
def move_part_to_cart():
    sid = request.cookies.get('current_order')
    data = json.loads(request.data)
    part = data['part']
    amount = data['amount']
    try:
        session_controller.add_part_to_cart(sid, part, amount)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=409)
    return jsonify('success')


@app.route('/api/make_order/submit_service', methods=['POST'])
@sid_required
@login_required
def move_service_to_cart():
    sid = request.cookies.get('current_order')
    data = json.loads(request.data)
    service = data['service']
    try:
        session_controller.add_part_to_cart(sid, service, service['amount'])
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=409)
    return jsonify('success')


@app.route('/api/make_order/submit_selection', methods=['POST'])
@sid_required
@login_required
def move_selection_to_cart():
    sid = request.cookies.get('current_order')
    try:
        session_controller.add_selection_to_cart(sid)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=409)
    return jsonify('success')


@app.route('/api/make_order/get_offer', methods=['POST'])
@sid_required
@login_required
def get_offer():
    sid = request.cookies.get('current_order')
    res = selection_controller.get_filtered_params(sid, request.form.get('only_present'))
    return jsonify(res)


@app.route('/api/make_order/suggest_part', methods=['POST'])
@sid_required
@login_required
def get_suggestion():
    sid = request.cookies.get('current_order')
    d = json.loads(request.data)
    only_present = d.get('only_present')
    res = selection_controller.get_suggestion(sid, only_present,
                                              d.get('part_params', {}),
                                              d.get('part_type'))
    return jsonify(res)


@app.route('/api/make_order/calc_part_price', methods=['POST'])
@sid_required
@login_required
def calc_part_price():
    sid = request.cookies.get('current_order')
    d = json.loads(request.data)
    part = d.get('part')
    type = d.get('job_type')
    res = price_controller.RVDPrice.calc_part_price(part, type)
    return jsonify(res.dict())


@app.route('/api/make_order/calc_item_price', methods=['POST'])
@sid_required
@login_required
def calc_item_price():
    sid = request.cookies.get('current_order')
    d = json.loads(request.data)
    part = d.get('part')
    amount = d.get('amount')
    res = price_controller.PartPrice.calc_part_price(part, amount)
    return jsonify(res.dict())


@app.route('/api/make_order/set_job_type', methods=['POST'])
@sid_required
@login_required
def set_job_type():
    sid = request.cookies.get('current_order')
    d = json.loads(request.data)
    return jsonify(selection_controller.set_job_type(sid, d.get('job_type')))


@app.route('/api/make_order/update_amount', methods=['POST'])
@sid_required
@login_required
def update_amount():
    sid = request.cookies.get('current_order')
    d = json.loads(request.data)
    return jsonify(selection_controller.update_amount(sid, d.get('amount')))


# ----------------CART ENDPOINTS---------------

@app.route('/api/make_order/get_cart', methods=['POST'])
@sid_required
@login_required
def get_cart():
    sid = request.cookies.get('current_order')
    cart = session_controller.get_cart(sid)
    return jsonify(cart)


@app.route('/api/make_order/del_cart_item', methods=['POST'])
@sid_required
@login_required
def del_cart_item():
    sid = request.cookies.get('current_order')
    data = json.loads(request.data)
    return jsonify(session_controller.del_cart_item(sid, data['id']))


@app.route('/api/make_order/get_carts', methods=['POST'])
@sid_required
@login_required
def get_carts():
    d = json.loads(request.data)
    sorting = d.get('sorting', None)
    carts = session_controller.get_user_sessions(current_user.username, sorting=sorting)
    return jsonify(carts)


@app.route('/api/make_order/checkout', methods=['POST'])
@sid_required
@login_required
def checkout_order_view():
    sid = request.cookies.get('current_order')
    try:
        order = order_controller.create_order(sid)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=409)
    session_controller.remove_session(sid)
    resp = make_response(jsonify(order.order_num))
    resp.delete_cookie('current_order')
    sessions = session_controller.get_user_sessions(current_user.username)['data']
    resp = make_response(jsonify({}))
    if len(sessions) != 0:
        resp.set_cookie('current_order', sessions[-1]['_id'])
    else:
        resp.delete_cookie('current_order')
    return resp


@app.route('/api/make_order/set_comment', methods=['POST'])
@sid_required
@login_required
def set_comment_view():
    sid = request.cookies.get('current_order')
    session_controller.set_comment(sid, json.loads(request.form.get('data', '')))
    return jsonify(session_controller.set_comment(sid, json.loads(request.form.get('data', '')))['comment'])


@app.route('/api/make_order/get_comment', methods=['POST'])
@sid_required
@login_required
def get_comment_view():
    sid = request.cookies.get('current_order')
    res = session_controller.get_comment(sid)
    return jsonify(res)


# ----------------CONTRAGENT ENDPOINTS---------------


@app.route('/api/contragent/create_contragent', methods=['POST'])
@login_required
def create_contragent():
    data = json.loads(request.form.get('data', []))
    try:
        contragent_controller.create_contragent_from_form(data)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=409)
    return jsonify('success')


@app.route('/api/contragent/find_contragents', methods=['POST'])
@login_required
def find_contragents():
    data = json.loads(request.data)
    query = data['query']
    return jsonify(contragent_controller.find_contragents(query))


# ----------------ADMIN ROUTES------------------


@app.route('/api/create_user', methods=['POST'])
# @login_required
def create_user():
    try:
        user_token = users_controller.create_user(**request.form)
        return jsonify('success')
    except ValueError as e:
        traceback.print_exc()
        resp = Response(str(e))
        resp.status = 409
        return resp
