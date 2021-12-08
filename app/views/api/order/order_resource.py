import traceback

from flask import jsonify
from flask_restful.reqparse import RequestParser

from app.core.controllers import order_controller
from app.views.api.common import ApiResource


class Order(ApiResource):

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('order_id', type=str)
        self.parser.add_argument('operation', type=str)

    # @orders.route('/get_order', methods=['POST'])
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        order_id = data['order_id']
        order = order_controller.get_order(order_id)
        return jsonify(order)

    # @orders.route('/<string:order_id>/close', methods=['POST'])
    # @login_required
    # @orders.route('/<string:order_id>/checkout', methods=['POST'])
    # @login_required
    def post(self):
        data = self.parser.parse_args()
        operation = data['operation']
        order_id = data['order_id']

        if operation == 'close':
            try:
                order = order_controller.close_order(order_id)
            except Exception as e:
                traceback.print_exc()
                return str(e), 409
            return jsonify(order)
        elif operation == 'checkout':
            try:
                order = order_controller.checkout_order(order_id)
            except Exception as e:
                traceback.print_exc()
                return str(e), 409
            return jsonify(order)
        else:
            return '', 404


class OrderUpd(ApiResource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('order_id', type=str)
        self.parser.add_argument('upd_num')

    # @orders.route('/<string:order_id>/set_upd', methods=['POST'])
    # @login_required
    def put(self):
        data = self.parser.parse_args()
        order_id = data['order_id']
        upd = data['upd_num']
        order = order_controller.set_upd(order_id, upd)
        return jsonify(order)

    # @orders.route('/<string:order_id>/download_upd', methods=['POST'])
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        order_id = data['order_id']
        return order_controller.get_upd(order_id)


class OrderBill(ApiResource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('order_id', type=str)

    # @orders.route('/<string:order_id>/download_bill', methods=['POST'])
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        order_id = data['order_id']
        return order_controller.get_bill(order_id)
