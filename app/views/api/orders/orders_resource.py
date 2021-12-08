from flask import jsonify
from flask_restful.reqparse import RequestParser

from app.core.controllers import order_controller
from app.views.api.common import ApiResource


class Orders(ApiResource):

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('limit', type=int)
        self.parser.add_argument('offset', type=int)
        self.parser.add_argument('sorting', type=str)

    # @orders.route('/get_orders', methods=['POST'])
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        limit = data['limit']
        offset = data['offset']
        sorting = data['sorting']
        orders = order_controller.get_all_orders(limit=limit, offset=offset, sorting=sorting)
        return jsonify(orders)
