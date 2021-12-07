import traceback

from flask import Blueprint, request, jsonify, Response

from app.core.controllers import users_controller

create_user = Blueprint('create_user_api', __name__)


@create_user.route('/', methods=['POST'])
# @login_required
def create_user_view():
    try:
        user_token = users_controller.create_user(**request.form)
        return jsonify('success')
    except ValueError as e:
        traceback.print_exc()
        resp = Response(str(e))
        resp.status = 409
        return resp
