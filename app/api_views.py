import json
import locale
import sys

import pytz
from flask import request, jsonify, make_response, abort, render_template
from flask_login import login_required, current_user
from mongoengine import QuerySet

from app import app
from app.base_views import sid_required, check_sid, remove_session_by_session
from app.core.controllers import selection_controller, session_controller, contragent_controller
from app.core.models.cart import Cart
from app.core.models.offer import RVDOffer
from app.core.models.order import Order
from app.core.models.user import User
from app.core.models.сontragent import Contragent
from app.core.sessions import *
# ----------------SESSION ENDPOINTS---------------
from app.utilities import orders_controller

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
    print(sessions)
    return jsonify(sessions)


@app.route('/api/orders/get_orders', methods=['POST'])
@login_required
def get_orders():
    orders = orders_controller.get_all_orders()
    print(orders)
    return jsonify(orders)


@app.route('/api/orders/get_order', methods=['POST'])
@login_required
def get_order():
    order_id = json.loads(request.form.get('data'))
    order = orders_controller.get_order_dict(order_id)
    return jsonify(order)


@app.route('/api/orders/<string:order_id>/set_upd', methods=['POST'])
@login_required
def set_upd(order_id):
    upd = json.loads(request.form.get('data'))
    order = orders_controller.set_upd(order_id, upd)
    return jsonify(order)


@app.route('/api/orders/<string:order_id>/download_upd', methods=['POST'])
@login_required
def download_upd(order_id):
    order = orders_controller.get_order(order_id)
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
    time = msk_timezone.localize(order.time_created)
    local_time = time.strftime("%d %B %Y г.")
    upd = render_template('UPD.htm', order=order.get_dict(),
                          items=order.cart.items,
                          date=local_time, day=time.strftime('%d'),
                          month=time.strftime('%B'),
                          year=time.strftime('%Y')[2:],
                          final_price=order._price)
    return upd


@app.route('/api/orders/<string:order_id>/close', methods=['POST'])
@login_required
def close_order(order_id):
    order = orders_controller.close_order(order_id)
    return jsonify(order)


# ----------------CREATE ORDER ENDPOINTS------------


@app.route('/api/make_order/update_selection_items', methods=['POST'])
@login_required
@sid_required
def update_session_view():
    sid = request.cookies.get('current_order')
    data = json.loads(request.form.get('data', []))
    return selection_controller.update_selection(sid, data)


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
    session = session_controller.get_session(sid)
    if 'contragent' in session.data:
        session.remove_data('contragent')
        session.save()
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


@app.route('/api/make_order/submit_selection', methods=['POST'])
@sid_required
@login_required
def move_selection_to_cart():
    sid = request.cookies.get('current_order')
    session = session_controller.get_session(sid)
    offer = RVDOffer(session)
    errors = offer.get_errors()
    if errors:
        return '\r\n'.join(errors)
    result = offer.create_cart_item(False)
    if not result:
        return 'success'


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
    return jsonify(session_controller.get_cart(sid))


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
    session = session_controller.get_session(request.cookies.get('current_order'))
    order = Order()
    try:
        order = Order.create_from_session(session)
    except NotImplementedError:
        abort(400, 'error was found')  # TODO: catch error message
    order.checkout_order()
    session_controller.remove_session(session.id)
    resp = make_response(order.order_num)
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
    contragent_controller.create_contragent_from_form(data)
    return jsonify('success')


@app.route('/api/contragent/find_contragents', methods=['POST'])
@login_required
def find_contragents():
    data = json.loads(request.form.get('data', []))
    return jsonify(contragent_controller.find_contragents(data))


# ----------------USER ROUTES------------------


@app.route('/api/create_user', methods=['POST'])
@login_required
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    surname = request.form.get('surname', '')
    role = request.form.get('role', '')
    try:
        user = User.create_user(username, password, name, surname, role)
        return user.get_id()
    except ValueError:
        abort(409, 'user already exists')
