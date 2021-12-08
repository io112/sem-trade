from flask import jsonify
from flask_login import current_user

from app.core.controllers import session_controller
from app.views.api.make_order.make_order_resource import MakeOrderBase


class OrderCarts(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('sorting', type=str)

    # @bp.route('/get_carts', methods=['POST'])
    # @sid_required
    # @login_required

    def get(self):
        data = self.parser.parse_args()
        sorting = data.get('sorting', None)
        carts = session_controller.get_user_sessions(current_user.username, sorting=sorting)
        return jsonify(carts)
