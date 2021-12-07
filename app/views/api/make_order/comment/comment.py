from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.comment.comment_resource import OrderComment

bp = Blueprint('order_comment_api', __name__)

api = Api(bp)

api.add_resource(OrderComment, '/')
