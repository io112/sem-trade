import pytz
from flask import request, redirect, url_for, Blueprint
from flask_login import login_user

from app import login_manager
from app.core.controllers.users_controller import login_using_token
from app.core.models.user import User
from app.views.frontend.auth import urls as auth_urls
from app.views.frontend.carts import urls as carts_urls
from app.views.frontend.create_order import urls as create_ord_urls
from app.views.frontend.create_user import urls as create_user_urls
from app.views.frontend.crm import crm
from app.views.frontend.order import urls as order_urls
from app.views.frontend.orders import urls as orders_urls

login_manager.login_view = 'frontend.auth.login'
msk_timezone = pytz.timezone('Europe/Moscow')


@login_manager.unauthorized_handler
def unauthorized():
    user_token = request.args.get('token')
    if user_token:
        res = login_using_token(user_token)
        if res is not None:
            login_user(res, remember=True)
            return redirect(url_for('frontend.create_order.create_order'))
    return redirect(url_for(login_manager.login_view))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


frontend = Blueprint('frontend', __name__, template_folder='templates')

frontend.register_blueprint(create_ord_urls.bp, url_prefix='/')
frontend.register_blueprint(crm.bp, url_prefix='/')
frontend.register_blueprint(carts_urls.bp, url_prefix='/my_sessions')
frontend.register_blueprint(orders_urls.bp, url_prefix='/orders')
frontend.register_blueprint(order_urls.bp, url_prefix='/order')
frontend.register_blueprint(create_user_urls.bp, url_prefix='/create_user')
frontend.register_blueprint(auth_urls.bp, url_prefix='/auth')
