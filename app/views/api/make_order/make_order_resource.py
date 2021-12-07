from flask import Response, make_response, jsonify
from flask_login import current_user
from flask_restful.reqparse import RequestParser

from app.core.controllers import session_controller
from app.core.sessions import start_session
from app.misc import sid_required
from app.views.api.common import ApiResource


class MakeOrderBase(ApiResource):
    method_decorators = [sid_required]

    CURRENT_ORDER_COOKIE = 'current_order'

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument(self.CURRENT_ORDER_COOKIE, location='cookies', required=True)


class MakeOrder(MakeOrderBase):

    def get(self):
        session = start_session(current_user.username)
        resp = Response()
        resp.set_cookie(self.CURRENT_ORDER_COOKIE, session.id)
        return resp

    # @bp.route('/cancel', methods=['POST'])
    # @login_required
    # @sid_required
    def delete(self):
        data = self.parser.parse_args()
        sid = data[self.CURRENT_ORDER_COOKIE]
        session_controller.remove_session(sid)
        sessions = session_controller.get_user_sessions(current_user.username)
        sessions = sessions['data']
        if len(sessions) > 0:
            resp = make_response(jsonify(''))
            resp.set_cookie(self.CURRENT_ORDER_COOKIE, sessions[0]['_id'])
            return resp
        else:
            resp = make_response(jsonify(''))
            session = start_session(current_user.username)
            resp.set_cookie(self.CURRENT_ORDER_COOKIE, session.id)
            return resp
