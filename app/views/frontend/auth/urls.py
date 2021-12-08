from flask import Blueprint

from app.views.frontend.auth.auth import LoginView, ChangePasswordView, LogoutView

bp = Blueprint('auth', __name__, template_folder='templates')
bp.add_url_rule('/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
bp.add_url_rule('/change_password', view_func=ChangePasswordView.as_view('change_password'))
