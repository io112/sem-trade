import json
import sys

import pytz
from flask import request, jsonify, make_response, abort, Response
from flask_login import login_required, current_user

from app import app
from app.core.controllers import order_controller, selection_controller, session_controller, contragent_controller, \
    users_controller
from app.core.models.user import User
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
    resp = make_response(jsonify(sessions))
    current_order = request.cookies.get('current_order')
    if current_order is not None and current_order == sid:
        if len(sessions) == 0:
            resp.delete_cookie('current_order')
        else:
            resp.set_cookie('current_order', sessions[0]['_id'])
    return resp


@app.route('/api/sessions/get_sessions', methods=['POST'])
@login_required
def get_sessions():
    sessions = session_controller.get_user_sessions(current_user.username)
    return jsonify(sessions)


@app.route('/api/orders/get_orders', methods=['POST'])
@login_required
def get_orders():
    limit = int(request.form.get('limit', 0))
    offset = int(request.form.get('offset', 0))
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


@app.route('/api/orders/<string:order_id>/close', methods=['POST'])
@login_required
def close_order(order_id):
    try:
        order = order_controller.close_order(order_id)
    except Exception as e:
        return Response(str(e), status=409)
    return jsonify(order)


@app.route('/api/orders/<string:order_id>/checkout', methods=['POST'])
@login_required
def checkout_order(order_id):
    try:
        order = order_controller.checkout_order(order_id)
    except Exception as e:
        return Response(str(e), status=409)
    return jsonify(order)


# ----------------CREATE ORDER ENDPOINTS------------


@app.route('/api/make_order/update_selection_items', methods=['POST'])
@login_required
@sid_required
def update_session_view():
    sid = request.cookies.get('current_order')
    data = json.loads(request.form.get('data', []))
    return selection_controller.update_selection(sid, data)


@app.route('/api/make_order/find_part', methods=['POST'])
@login_required
@sid_required
def find_part():
    data = json.loads(request.form.get('data', []))

    res = selection_controller.find_part(data[0]['value'], data[1]['value'])
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
    if len(sessions) > 0:
        return jsonify(sessions[-1]['_id'])
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
    contragent_id = json.loads(request.form.get('data', []))
    try:
        session_controller.set_contragent(sid, contragent_id)
        return contragent_controller.get_contragent(contragent_id)
    except Exception:
        print(sys.exc_info()[0])
        return str(sys.exc_info()[0]), 404


@app.route('/api/make_order/get_contragent', methods=['POST'])
@sid_required
@login_required
def get_contragent():
    sid = request.cookies.get('current_order')
    try:
        contragent = session_controller.get_contragent(sid)
        return contragent
    except Exception:
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
    try:
        session_controller.add_part_to_cart(sid)
    except Exception as e:
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
        return Response(str(e), status=409)
    return jsonify('success')


@app.route('/api/make_order/get_offer', methods=['POST'])
@sid_required
@login_required
def get_offer():
    sid = request.cookies.get('current_order')
    res = selection_controller.get_filtered_params(sid)
    # if errors:
    #     return '\r\n'.join(errors)
    # result = offer.create_cart_item(False)
    # if not result:
    #     return 'success'
    return jsonify(res)


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
    data = json.loads(request.form.get('data', []))
    return jsonify(session_controller.del_cart_item(sid, data['id']))


@app.route('/api/make_order/get_carts', methods=['POST'])
@sid_required
@login_required
def get_carts():
    carts = session_controller.get_user_sessions(current_user.username)
    return jsonify(carts)


@app.route('/api/make_order/checkout', methods=['POST'])
@sid_required
@login_required
def checkout_order_view():
    sid = request.cookies.get('current_order')
    try:
        order = order_controller.create_order(sid)
    except Exception as e:
        return Response(str(e), status=409)
    session_controller.remove_session(sid)
    resp = make_response(jsonify(order.order_num))
    resp.delete_cookie('current_order')

    # return Response(result,
    #                 mimetype="application/xml",
    #                 headers={"Content-Disposition": "attachment;filename=orders.xml"})
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
        return Response(str(e), status=409)
    return jsonify('success')


@app.route('/api/contragent/find_contragents', methods=['POST'])
@login_required
def find_contragents():
    data = json.loads(request.form.get('data', []))
    return jsonify(contragent_controller.find_contragents(data))


# ----------------ADMIN ROUTES------------------


@app.route('/api/create_user', methods=['POST'])
@login_required
def create_user():
    try:
        user_token = users_controller.create_user(**request.form)
        return jsonify('success')
    except ValueError as e:
        resp = Response(str(e))
        resp.status = 409
        return resp
