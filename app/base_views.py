import functools
import sys

from flask import request, render_template, redirect, url_for, jsonify, make_response, abort, Response
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse

from app.constants import *
from app.core.models.сontragent import Contragent
from app.core.models.cart import Cart
from app.core.models.offer import RVDOffer
from app.core.models.user import User
from app.crm import base
from app import app, login_manager
from werkzeug.security import check_password_hash
from app.core.sessions import *
import json

auth = HTTPBasicAuth()
login_manager.login_view = 'login_route'


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


def remove_session_by_session(session):
    cart = Cart.create_from_session(session)
    cart.remove_cart()
    session.remove_data('cart')
    remove_session(session.get_id())


@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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
@login_required
def home():
    sid = request.cookies.get('current_order')
    session = get_session(sid)
    offer = RVDOffer(session).to_dict()
    return render_template('create_order/create_order.html', items=[testitem], offer=offer, user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/my_sessions', methods=['GET'])
@login_required
def my_sessions():
    return render_template('incompleted_orders.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        user: User
        if user is not None and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
    return render_template('login.html')


# -----------------[1C ROUTES]-----------------

@app.route('/bitrix/admin/1c_exchange.php', methods=['GET', 'POST'])
@auth.login_required
def exchange():
    return Response(base.router(request.args, request.data), mimetype='text/xml')
