from flask import jsonify
from flask_login import current_user
from flask_restful.reqparse import RequestParser

from app.core.controllers import session_controller
from app.views.api.common import ApiResource


class Carts(ApiResource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('cart_id', type=str)
        self.parser.add_argument('limit', type=int)
        self.parser.add_argument('offset', type=int)
        self.parser.add_argument('sorting', type=str)

    # @sessions.route('/remove_session', methods=['POST'])
    # @login_required
    def delete(self):
        data = self.parser.parse_args()
        sid = data['cart_id']
        session_controller.remove_session(sid)
        sessions = session_controller.get_user_sessions(current_user.username)
        return jsonify(sessions)

    # @sessions.route('/get_sessions', methods=['POST'])
    # @login_required
    def get(self):
        data = self.parser.parse_args()
        limit = data['limit']
        offset = data['offset']
        sorting = data['sorting']
        sessions = session_controller.get_user_sessions(current_user.username, limit=limit, offset=offset,
                                                        sorting=sorting)
        return jsonify(sessions)
