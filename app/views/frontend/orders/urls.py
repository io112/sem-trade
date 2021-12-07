from flask import Blueprint

from app.views.frontend.orders.orders import OrdersView

bp = Blueprint('orders', __name__, template_folder='templates')

bp.add_url_rule('/', view_func=OrdersView.as_view('orders'))

