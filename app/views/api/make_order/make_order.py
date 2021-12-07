from flask import Blueprint, request, jsonify, make_response
from flask_login import login_required, current_user
from flask_restful import Api

from app.core.controllers import session_controller
from app.misc import sid_required
from app.views.api.make_order.cart import cart
from app.views.api.make_order.carts import carts
from app.views.api.make_order.checkout import checkout
from app.views.api.make_order.comment import comment
from app.views.api.make_order.contragent import contragent
from app.views.api.make_order.make_order_resource import MakeOrderBase
from app.views.api.make_order.part_selection import part_selection
from app.views.api.make_order.rvd_selection import rvd_selection
from app.views.api.make_order.service import service

bp = Blueprint('make_order_api', __name__)
bp.register_blueprint(rvd_selection.bp, url_prefix='selection')
bp.register_blueprint(part_selection.bp, url_prefix='part')
bp.register_blueprint(cart.bp, url_prefix='cart')
bp.register_blueprint(contragent.bp, url_prefix='contragent')
bp.register_blueprint(service.bp, url_prefix='service')
bp.register_blueprint(checkout.bp, url_prefix='checkout')
bp.register_blueprint(comment.bp, url_prefix='comment')
bp.register_blueprint(carts.bp, url_prefix='carts')

api = Api(bp)
api.add_resource(MakeOrderBase)


@bp.route('/cancel', methods=['POST'])
@login_required
@sid_required
def remove_order():
    sid = request.cookies.get('current_order')
    session_controller.remove_session(sid)
    sessions = session_controller.get_user_sessions(current_user.username)
    sessions = sessions['data']
    if len(sessions) > 0:
        return jsonify(sessions[0]['_id'])
    else:
        resp = make_response(jsonify(''))
        resp.delete_cookie('current_order')
        return resp
