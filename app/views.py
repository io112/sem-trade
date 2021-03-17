import sys

from flask import request, render_template, redirect, url_for, jsonify
import json
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


@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


testitem = {'name': 'testitem', 'amount': 5, 'price': 500}
testoffer = {'arms': [{'diameter': 5}, {'diameter': 10}]}


@app.route('/', methods=['GET'])
def home():
    sid = request.args.get('sid')
    cs = check_sid(sid)
    if not cs:
        return redirect(url_for('home', sid=start_session().get_id()))
    session = get_session(sid)
    offer = RVDOffer(session).to_dict()
    return render_template('create_order/create_order.html', items=[testitem], offer=offer)


@app.route('/api/update_session', methods=['POST'])
def update_session_view():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
    data = json.loads(request.form.get('data', []))
    session = get_session(sid)
    session.add_data(data)
    update_session(session)
    return 'success'


@app.route('/api/update_selection', methods=['POST'])
def update_select():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
    session = get_session(sid)
    offer = RVDOffer(session).to_dict()
    offer_string = json.dumps(offer).encode('utf-8')
    return offer_string


@app.route('/api/submit_selection', methods=['POST'])
def move_selection_to_cart():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
    session = get_session(sid)
    offer = RVDOffer(session)
    errors = offer.get_errors()
    if errors:
        return '\r\n'.join(errors)
    result = offer.create_cart_item(False)
    if not result:
        return 'success'


@app.route('/api/get_cart', methods=['POST'])
def get_cart():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
    session = get_session(sid)
    cart = Cart.create_from_session(session)
    return jsonify(cart.__get__())


@app.route('/api/del_cart_item', methods=['POST'])
def del_cart_item():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
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
def set_contragent():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
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
def get_contragent():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
    session = get_session(sid)
    try:
        contragent = Contragent.create_from_session(session)
        return contragent.get()
    except Exception:
        print(sys.exc_info()[0])
        return jsonify({})


@app.route('/api/remove_contragent', methods=['POST'])
def remove_contragent():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
    session = get_session(sid)
    if 'contragent' in session.data:
        session.remove_data('contragent')
        update_session(session)
    return jsonify({})


@app.route('/bitrix/admin/1c_exchange.php', methods=['GET', 'POST'])
@auth.login_required
def exchange():
    return base.router(request.args, request.data)
