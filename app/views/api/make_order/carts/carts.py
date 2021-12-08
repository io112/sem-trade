from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.carts.carts_resource import OrderCarts

bp = Blueprint('order_carts_api', __name__)

api = Api(bp)

api.add_resource(OrderCarts, '/')
