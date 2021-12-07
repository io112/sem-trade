import json

from flask import Blueprint, request, abort, make_response, jsonify
from flask_login import login_required, current_user

from app.core.controllers import session_controller
from app.misc import check_sid

sessions = Blueprint('sessions_api', __name__)


@sessions.route('/remove_session', methods=['POST'])
@login_required
def remove_session_view():
    sid = json.loads(request.form.get('data'))
    if sid is None:
        abort(404, 'sid not found')
    if not check_sid(sid):
        abort(404, 'session not found')
    session_controller.remove_session(sid)
    sessions = session_controller.get_user_sessions(current_user.username)
    sessions = sessions
    resp = make_response(jsonify(sessions))
    current_order = request.cookies.get('current_order')
    if current_order is not None and current_order == sid:
        if len(sessions) == 0:
            resp.delete_cookie('current_order')
        else:
            resp.set_cookie('current_order', sessions['data'][0]['_id'])
    return resp


@sessions.route('/get_sessions', methods=['POST'])
@login_required
def get_sessions_view():
    d = json.loads(request.data)
    limit = int(d.get('limit', 0))
    offset = int(d.get('offset', 0))
    sessions = session_controller.get_user_sessions(current_user.username, limit=limit, offset=offset)
    return jsonify(sessions)
