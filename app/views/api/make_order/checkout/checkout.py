from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.checkout.checkout_resource import OrderCheckout

bp = Blueprint('order_checkout_api', __name__)

api = Api(bp)

api.add_resource(OrderCheckout, '/')
