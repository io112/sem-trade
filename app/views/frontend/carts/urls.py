from flask import Blueprint

from app.views.frontend.carts.carts import CartsView

bp = Blueprint('carts', __name__, template_folder='templates')
bp.add_url_rule('/', view_func=CartsView.as_view('carts'))
