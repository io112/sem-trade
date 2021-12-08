import traceback

from app.core.controllers import session_controller
from app.views.api.make_order.make_order_resource import MakeOrderBase


class SubmitService(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('service', type=dict)

    # @bp.route('/submit_service', methods=['POST'])
    # @sid_required
    # @login_required
    def post(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        service = data['service']
        try:
            session_controller.add_part_to_cart(sid, service, service['amount'])
        except Exception as e:
            traceback.print_exc()
            return str(e), 409
        return 'success'
