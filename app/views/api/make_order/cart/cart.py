from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.cart.cart_resource import OrderCart

bp = Blueprint('order_cart_api', __name__)

api = Api(bp)

api.add_resource(OrderCart, '/')
