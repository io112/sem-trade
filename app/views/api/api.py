from flask import Blueprint

from app.views.api.contragent import contragent
from app.views.api.create_user import create_user
from app.views.api.make_order import make_order
from app.views.api.orders import orders
from app.views.api.order import order
from app.views.api.carts import carts

api = Blueprint('api', __name__)
api.register_blueprint(carts.bp, url_prefix='sessions')
api.register_blueprint(orders.bp, url_prefix='orders')
api.register_blueprint(order.bp, url_prefix='order')
api.register_blueprint(make_order.bp, url_prefix='make_order')
api.register_blueprint(contragent.bp, url_prefix='contragent')
api.register_blueprint(create_user, url_prefix='create_user')
