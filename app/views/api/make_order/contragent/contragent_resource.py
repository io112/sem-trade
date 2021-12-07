import sys
import traceback

from app.core.controllers import session_controller, contragent_controller
from app.views.api.make_order.make_order_resource import MakeOrderBase


class OrderContragent(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('id', type=str)

    # @bp.route('/remove_contragent', methods=['POST'])
    # @login_required
    # @sid_required
    def delete(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        session_controller.del_contragent(sid)
        return {}

    # @bp.route('/set_contragent', methods=['POST'])
    # @login_required
    # @sid_required
    def put(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        contragent_id = data['id']
        try:
            session_controller.set_contragent(sid, contragent_id)
            return contragent_controller.get_contragent(contragent_id)
        except Exception as e:
            traceback.print_exc()
            return str(sys.exc_info()[0]), 404

    # @bp.route('/get_contragent', methods=['POST'])
    # @sid_required
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        try:
            contragent = session_controller.get_contragent(sid)
            return contragent
        except Exception as e:
            traceback.print_exc()
            return {}
