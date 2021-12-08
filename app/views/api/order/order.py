from flask import Blueprint
from flask_restful import Api

from app.views.api.order.order_resource import Order, OrderBill, OrderUpd

bp = Blueprint('order_api', __name__)
api = Api(bp)
api.add_resource(Order, '/')
api.add_resource(OrderBill, '/bill')
api.add_resource(OrderUpd, '/upd')
