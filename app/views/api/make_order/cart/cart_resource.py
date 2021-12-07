from app.core.controllers import session_controller
from app.views.api.make_order.make_order_resource import MakeOrderBase


class OrderCart(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('id', type='str')

    # @bp.route('/get_cart', methods=['POST'])
    # @sid_required
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        cart = session_controller.get_cart(sid)
        return cart

    # @bp.route('/del_cart_item', methods=['POST'])
    # @sid_required
    # @login_required
    def delete(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        return session_controller.del_cart_item(sid, data['id'])
