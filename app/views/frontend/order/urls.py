from flask import Blueprint

from app.views.frontend.order.order import OrderView, OrderUpdView, OrderBillView

bp = Blueprint('order', __name__, template_folder='templates')


bp.add_url_rule('/<string:order_id>', view_func=OrderView.as_view('order'))
bp.add_url_rule('/<string:order_id>/upd', view_func=OrderUpdView.as_view('order_upd'))
bp.add_url_rule('/<string:order_id>/bill', view_func=OrderBillView.as_view('order_bill'))