import traceback

from app.core.controllers import selection_controller, price_controller, session_controller
from app.views.api.make_order.make_order_resource import MakeOrderBase


class MakeOrderSelection(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('part', type=dict)
        self.parser.add_argument('type', type=str)
        self.parser.add_argument('item_index', type=int)

    # @bp.route('/add_item_to_selection', methods=['POST'])
    # @login_required
    # @sid_required
    def post(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        return selection_controller.add_item_to_selection(sid, data['part'], data['type'])

    # @bp.route('/del_selected_part', methods=['POST'])
    # @login_required
    # @sid_required
    def delete(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        return selection_controller.del_item_from_selection(sid, data['item_index'])

    # @bp.route('/update_selection', methods=['POST'])
    # @sid_required
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        return selection_controller.get_selection(sid)


class SelectionPartSearch(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('only_present', type=bool)
        self.parser.add_argument('part_params', type=dict)
        self.parser.add_argument('part_type', type=str)

    # @bp.route('/suggest_part', methods=['POST'])
    # @sid_required
    # @login_required
    def post(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        only_present = data['only_present']
        part_params = data['part_params']
        part_type = data['part_type']
        res = selection_controller.get_suggestion(sid, only_present, part_params, part_type)
        return res


class SelectionPartCalcPrice(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('part', type=dict)
        self.parser.add_argument('job_type', type=str)

    # @bp.route('/calc_part_price', methods=['POST'])
    # @sid_required
    # @login_required
    def post(self):
        data = self.parser.parse_args()
        part = data.get('part')
        type = data.get('job_type')
        res = price_controller.RVDPrice.calc_part_price(part, type)
        return res.dict()


class SelectionJobType(MakeOrderBase):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('job_type', type=str)

    # @bp.route('/set_job_type', methods=['POST'])
    # @sid_required
    # @login_required
    def put(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        return selection_controller.set_job_type(sid, data.get('job_type'))


class SelectionAmount(MakeOrderSelection):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('amount', type=int)

    # @bp.route('/update_amount', methods=['POST'])
    # @sid_required
    # @login_required
    def put(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        return selection_controller.update_amount(sid, data.get('amount'))


class SelectionSubmit(MakeOrderSelection):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('amount', type=int)

    # @bp.route('/submit_selection', methods=['POST'])
    # @sid_required
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        try:
            session_controller.add_selection_to_cart(sid)
        except Exception as e:
            traceback.print_exc()
            return {str(e)}, 409
        return 'success'
