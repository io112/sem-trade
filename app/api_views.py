import json
import sys

from flask import request, jsonify, make_response, abort

from app import app
from app.base_views import sid_required, check_sid, remove_session_by_session

from flask_login import login_user, current_user, login_required, logout_user

from app.core.models.сontragent import Contragent
from app.core.models.cart import Cart
from app.core.models.offer import RVDOffer
from app.core.sessions import *


@app.route('/api/update_session', methods=['POST'])
@sid_required
@login_required
def update_session_view():
    sid = request.cookies.get('current_order')
    data = json.loads(request.form.get('data', []))
    session = get_session(sid)
    session.add_data(data)
    update_session(session)
    return 'success'


@app.route('/api/update_selection', methods=['POST'])
@sid_required
@login_required
def update_select():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    offer = RVDOffer(session).to_dict()
    offer_string = json.dumps(offer).encode('utf-8')
    return offer_string


@app.route('/api/submit_selection', methods=['POST'])
@sid_required
@login_required
def move_selection_to_cart():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    offer = RVDOffer(session)
    errors = offer.get_errors()
    if errors:
        return '\r\n'.join(errors)
    result = offer.create_cart_item(False)
    if not result:
        return 'success'


@app.route('/api/get_cart', methods=['POST'])
@sid_required
@login_required
def get_cart():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    cart = Cart.create_from_session(session)
    return jsonify(cart.__get__())


@app.route('/api/del_cart_item', methods=['POST'])
@sid_required
@login_required
def del_cart_item():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    cart = Cart.create_from_session(session)
    data = json.loads(request.form.get('data', []))
    del cart[data['id']]
    cart.save(session)
    return jsonify(cart.__get__())


@app.route('/api/create_contragent', methods=['POST'])
@login_required
def create_contragent():
    data = json.loads(request.form.get('data', []))
    contragent = Contragent.create_from_form(data)
    print(contragent.__get__())
    contragent.save_to_db()
    return 'success'


@app.route('/api/find_contragents', methods=['POST'])
@login_required
def find_contragents():
    data = json.loads(request.form.get('data', []))
    return jsonify(Contragent.find_contragents(data))


@app.route('/api/set_contragent', methods=['POST'])
@sid_required
@login_required
def set_contragent():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    contragent_id = json.loads(request.form.get('data', []))
    try:
        contragent = Contragent.create_by_id(contragent_id)
        contragent.save_to_session(session)
        return contragent.get()
    except Exception:
        print(sys.exc_info()[0])
        return str(sys.exc_info()[0]), 404


@app.route('/api/get_contragent', methods=['POST'])
@sid_required
@login_required
def get_contragent():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    try:
        contragent = Contragent.create_from_session(session)
        return contragent.get()
    except Exception:
        print(sys.exc_info()[0])
        return jsonify({})


@app.route('/api/remove_contragent', methods=['POST'])
@sid_required
@login_required
def remove_contragent():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    if 'contragent' in session.data:
        session.remove_data('contragent')
        update_session(session)
    return jsonify({})


@app.route('/api/get_carts', methods=['POST'])
@sid_required
@login_required
def get_carts():
    carts = get_session_ids()
    print(carts)
    return jsonify(carts)


@app.route('/api/remove_order', methods=['POST'])
@sid_required
@login_required
def remove_order():
    session = get_session(request.cookies.get('current_order'))
    remove_session_by_session(session)
    if len(get_session_ids()) > 0:
        return get_session_ids()[-1]['_id']
    else:
        resp = make_response('')
        resp.delete_cookie('current_order')
        return resp


@app.route('/api/remove_session', methods=['POST'])
@login_required
def route_remove_session():
    sid = json.loads(request.form.get('data'))
    if sid is None:
        abort(404, 'sid not found')
    if not check_sid(sid):
        abort(404, 'session not found')
    remove_session_by_session(get_session(sid))
    sessions = get_user_sessions(fields=['_id', 'user', 'last_modified'])
    resp = make_response(jsonify(sessions))
    if request.cookies.get('current_order') is not None and request.cookies.get('current_order') == sid:
        if len(sessions) == 0:
            resp.delete_cookie('current_order')
        else:
            resp.set_cookie('current_order', sessions[0]['_id'])
    print(sessions)
    return resp


@app.route('/api/get_sessions', methods=['POST'])
@login_required
def get_sessions():
    sessions = get_user_sessions(fields=['_id', 'user', 'last_modified'])
    print(sessions)
    return jsonify(sessions)
