from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.contragent.contragent_resource import OrderContragent

bp = Blueprint('order_contragent_api', __name__)

api = Api(bp)

api.add_resource(OrderContragent, '/')
