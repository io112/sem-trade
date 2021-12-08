from flask import Blueprint

from app.views.frontend.create_order.create_order import CreateOrderView

bp = Blueprint('create_order', __name__, template_folder='templates')
bp.add_url_rule('/', view_func=CreateOrderView.as_view('create_order'))
