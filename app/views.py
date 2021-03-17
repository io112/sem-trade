import functools
import sys

from flask import request, render_template, redirect, url_for, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from app.constants import *
from app.core.models.Contragent import Contragent
from app.core.models.cart import Cart
from app.core.models.offer import RVDOffer
from app.crm import base
from app import app
from werkzeug.security import check_password_hash
from app.core.sessions import *
import json

auth = HTTPBasicAuth()


def check_sid(sid):
    if sid is None:
        return False
    elif not check_session(sid):
        return False
    return True


def make_cookie_resp(url, sid=None):
    if sid:
        resp = make_response(redirect(url_for(url)))
        resp.set_cookie('current_order', sid)
    else:
        session = start_session()
        resp = make_response(redirect(url_for(url)))
        resp.set_cookie('current_order', session.get_id())
    return resp


@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


def sid_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        sid = request.args.get('sid', None)
        if sid is not None:
            cs = check_sid(sid)
            if cs:
                resp = make_cookie_resp('home', sid)
            else:
                resp = make_cookie_resp('home')
            return resp
        sid = request.cookies.get('current_order')
        if not check_sid(sid):
            return make_cookie_resp('home')
        return view(**kwargs)

    return wrapped_view


testitem = {'name': 'testitem', 'amount': 5, 'price': 500}
testoffer = {'arms': [{'diameter': 5}, {'diameter': 10}]}


@app.route('/', methods=['GET'])
@sid_required
def home():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    offer = RVDOffer(session).to_dict()
    return render_template('create_order/create_order.html', items=[testitem], offer=offer)


@app.route('/api/update_session', methods=['POST'])
@sid_required
def update_session_view():
    sid = request.cookies.get('current_order')
    data = json.loads(request.form.get('data', []))
    session = get_session(sid)
    session.add_data(data)
    update_session(session)
    return 'success'


@app.route('/api/update_selection', methods=['POST'])
@sid_required
def update_select():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    offer = RVDOffer(session).to_dict()
    offer_string = json.dumps(offer).encode('utf-8')
    return offer_string


@app.route('/api/submit_selection', methods=['POST'])
@sid_required
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
def get_cart():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    cart = Cart.create_from_session(session)
    return jsonify(cart.__get__())


@app.route('/api/del_cart_item', methods=['POST'])
@sid_required
def del_cart_item():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    cart = Cart.create_from_session(session)
    data = json.loads(request.form.get('data', []))
    del cart[data['id']]
    cart.save(session)
    return jsonify(cart.__get__())


@app.route('/api/create_contragent', methods=['POST'])
def create_contragent():
    data = json.loads(request.form.get('data', []))
    contragent = Contragent.create_from_form(data)
    print(contragent.__get__())
    contragent.save_to_db()
    return 'success'


@app.route('/api/find_contragents', methods=['POST'])
def find_contragents():
    data = json.loads(request.form.get('data', []))
    return jsonify(Contragent.find_contragents(data))


@app.route('/api/set_contragent', methods=['POST'])
@sid_required
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
def remove_contragent():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    if 'contragent' in session.data:
        session.remove_data('contragent')
        update_session(session)
    return jsonify({})


@app.route('/api/get_carts', methods=['POST'])
@sid_required
def get_carts():
    carts = get_session_ids()
    print(carts)
    return jsonify(carts)


@app.route('/api/remove_order', methods=['POST'])
@sid_required
def remove_order():
    session = get_session(request.cookies.get('current_order'))
    cart = Cart.create_from_session(session)
    cart.remove_cart()
    session.remove_data('cart')
    remove_session(session.get_id())
    if len(get_session_ids()) > 0:
        return get_session_ids()[-1]['_id']
    else:
        resp = make_response('')
        resp.delete_cookie('current_order')
        return resp


@app.route('/bitrix/admin/1c_exchange.php', methods=['GET', 'POST'])
@auth.login_required
def exchange():
    return base.router(request.args, request.data)
