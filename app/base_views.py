import functools

import pytz
from flask import request, render_template, redirect, url_for, make_response
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse

from app import app, login_manager
from app.constants import *
from app.core.controllers import order_controller
from app.core.models.user import User
from app.core.sessions import *
from app.crm import base
from app.misc import sid_required

auth = HTTPBasicAuth()
login_manager.login_view = 'login_route'
msk_timezone = pytz.timezone('Europe/Moscow')




@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


testitem = {'name': 'testitem', 'amount': 5, 'price': 500}
testoffer = {'arms': [{'diameter': 5}, {'diameter': 10}]}


@app.route('/', methods=['GET'])
@login_required
@sid_required
def home():
    return render_template('create_order/create_order.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/my_sessions', methods=['GET'])
@login_required
def my_sessions():
    return render_template('incompleted_orders.html', user=current_user)


@app.route('/orders', methods=['GET'])
@login_required
def orders():
    return render_template('orders.html', user=current_user)


@app.route('/orders/<string:order_id>', methods=['GET'])
@login_required
def order(order_id):
    return render_template('order.html', user=current_user)


@app.route('/orders/<string:order_id>/upd', methods=['GET'])
@login_required
def upd(order_id):
    return order_controller.get_upd(order_id)


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
    return base.router(request.args, request.data)
