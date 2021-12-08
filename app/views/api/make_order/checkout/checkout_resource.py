import traceback

from flask import make_response, jsonify
from flask_login import current_user

from app.core.controllers import order_controller, session_controller
from app.core.sessions import start_session
from app.views.api.make_order.make_order_resource import MakeOrderBase


class OrderCheckout(MakeOrderBase):

    # @bp.route('/checkout', methods=['POST'])
    # @sid_required
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        try:
            order = order_controller.create_order(sid)
        except Exception as e:
            traceback.print_exc()
            return str(e), 409
        session_controller.remove_session(sid)
        resp = make_response(jsonify(order.order_num))
        resp.delete_cookie('current_order')
        sessions = session_controller.get_user_sessions(current_user.username)['data']
        if len(sessions) != 0:
            resp.set_cookie('current_order', sessions[-1]['_id'])
        else:
            session = start_session(current_user.username)
            resp.set_cookie('current_order', session.id)
        return resp
