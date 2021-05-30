import functools
import sys

import pytz
from flask import request, render_template, redirect, url_for, make_response
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse

from app import app, login_manager
from app.constants import *
from app.core.controllers import order_controller, users_controller
from app.core.controllers.users_controller import login_using_token
from app.core.models.user import User
from app.core.sessions import *
from app.crm import base
from app.misc import sid_required, redirect_restore_pass

auth = HTTPBasicAuth()
login_manager.login_view = 'login_route'
msk_timezone = pytz.timezone('Europe/Moscow')


@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


# @login_manager.request_loader
# def load_user_from_request(request):
#     user_token = request.args.get('token')
#     if user_token:
#         res = login_using_token(user_token)
#         if res is not None:
#             login_user(res, remember=True)
#         return res
#     return None


@login_manager.unauthorized_handler
def unauthorized():
    user_token = request.args.get('token')
    if user_token:
        res = login_using_token(user_token)
        if res is not None:
            login_user(res, remember=True)
            return redirect(url_for('home'))
    return redirect(url_for(login_manager.login_view))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


testitem = {'name': 'testitem', 'amount': 5, 'price': 500}
testoffer = {'arms': [{'diameter': 5}, {'diameter': 10}]}


@app.route('/', methods=['GET'])
@login_required
@redirect_restore_pass
@sid_required
def home():
    return render_template('create_order/create_order.html', user=current_user, commit_hash=commit_hash)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/my_sessions', methods=['GET'])
@login_required
@redirect_restore_pass
def my_sessions():
    return render_template('incompleted_orders.html', user=current_user, commit_hash=commit_hash)


@app.route('/orders', methods=['GET'])
@login_required
@redirect_restore_pass
def orders():
    return render_template('orders.html', user=current_user, commit_hash=commit_hash)


@app.route('/orders/<string:order_id>', methods=['GET'])
@login_required
@redirect_restore_pass
def order(order_id):
    return render_template('order.html', user=current_user, commit_hash=commit_hash)


@app.route('/orders/<string:order_id>/upd', methods=['GET'])
@login_required
def upd(order_id):
    return order_controller.get_upd(order_id)

@app.route('/orders/<string:order_id>/bill', methods=['GET'])
@login_required
def bill(order_id):
    return order_controller.get_bill(order_id)


@app.route('/create_user', methods=['GET'])
@login_required
@redirect_restore_pass
def create_user_view():
    return render_template('create_user.html', user=current_user, commit_hash=commit_hash)


@app.route('/login/change_password', methods=['POST', 'GET'])
@login_required
def login_change_pass():
    if request.method == 'POST':
        try:
            users_controller.change_password(user=current_user, **request.form)
        except Exception as e:
            print(e.args)
            return render_template('login_change_password.html',
                                   error=str(e), user=current_user,
                                   commit_hash=commit_hash)

    if not current_user.change_password:
        return redirect(url_for('home'))
    return render_template('login_change_password.html', user=current_user, commit_hash=commit_hash)


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
    elif current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('login.html', commit_hash=commit_hash)

    # -----------------[1C ROUTES]-----------------


@app.route('/bitrix/admin/1c_exchange.php', methods=['GET', 'POST'])
@auth.login_required
def exchange():
    return base.router(request.args, request.data)
