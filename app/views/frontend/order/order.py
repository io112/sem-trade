from flask_login import current_user
from flask_restful import url_for
from flask_restful.reqparse import RequestParser

from app.constants import commit_hash
from app.core.controllers import order_controller
from app.views.frontend.base import BaseAuthView


class OrderView(BaseAuthView):
    template_name = 'order.html'

    def __init__(self):
        self.api_urls = {
            "API_ORDER_GET": url_for('order_api.Order'.lower()),
            "API_ORDER_MAKE_OP": url_for('order_api.Order'.lower()),
            "API_ORDER_BILL_GET": url_for('order_api.OrderBill'.lower()),
            "API_ORDER_UPD_GET": url_for('order_api.OrderUpd'.lower()),
            "API_ORDER_UPD_SET": url_for('order_api.OrderUpd'.lower()),
        }

    # @orders.route('/<string:order_id>', methods=['GET'])
    # @login_required
    # @redirect_restore_pass
    def dispatch_request(self, order_id):
        context = {
            'user': current_user,
            'commit_hash': commit_hash
        }
        return self.render_template(context)


class OrderUpdView(BaseAuthView):
    # @orders.route('/<string:order_id>/upd', methods=['GET'])
    # @login_required

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('order_id', type=str)

    def dispatch_request(self):
        order_id = self.parser.parse_args()['order_id']
        return order_controller.get_upd(order_id)


class OrderBillView(BaseAuthView):
    # @orders.route('/<string:order_id>/bill', methods=['GET'])
    # @login_required
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('order_id', type=str)

    def dispatch_request(self):
        order_id = self.parser.parse_args()['order_id']
        return order_controller.get_bill(order_id)
