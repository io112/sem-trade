from app.core.controllers import session_controller
from app.views.api.make_order.make_order_resource import MakeOrderBase


class OrderComment(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('comment', type=str)

    # @bp.route('/set_comment', methods=['POST'])
    # @sid_required
    # @login_required
    def post(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        comment = session_controller.set_comment(sid, data['comment'])['comment']
        return comment

    # @bp.route('/get_comment', methods=['POST'])
    # @sid_required
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        res = session_controller.get_comment(sid)
        return res
