from flask import Blueprint

from app.views.frontend.create_user.create_user import CreateUserView

bp = Blueprint('create_user', __name__, template_folder='templates')
bp.add_url_rule('/', view_func=CreateUserView.as_view('create_user'))
