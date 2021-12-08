import traceback

from app.core.controllers import selection_controller, price_controller, session_controller
from app.views.api.make_order.make_order_resource import MakeOrderBase


class PartSearch(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('query', type=str)
        self.parser.add_argument('only_present', type=bool)
        self.parser.add_argument('amount', type=int)

    # @bp.route('/find_part', methods=['POST'])
    # @login_required
    # @sid_required
    def post(self):
        data = self.parser.parse_args()
        res = selection_controller.find_part(data['query'], data.get('only_present'),
                                             data.get('amount', 1))
        return res


class PartPrice(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('part', type=dict)
        self.parser.add_argument('amount', type=int)

    # @bp.route('/calc_item_price', methods=['POST'])
    # @sid_required
    # @login_required
    def post(self):
        data = self.parser.parse_args()
        part = data.get('part')
        amount = data.get('amount')
        res = price_controller.PartPrice.calc_part_price(part, amount)
        return res.dict()


class PartSubmit(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('part', type=dict)
        self.parser.add_argument('amount', type=int)

    # @bp.route('/submit_part', methods=['POST'])
    # @sid_required
    # @login_required
    def post(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        part = data['part']
        amount = data['amount']
        try:
            session_controller.add_part_to_cart(sid, part, amount)
        except Exception as e:
            traceback.print_exc()
            return str(e), 409
        return 'success'
