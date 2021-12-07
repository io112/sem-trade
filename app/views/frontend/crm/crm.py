from flask import Blueprint, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from app.constants import site_login, site_password
from app.crm import base

bp = Blueprint('crm', __name__, template_folder='templates')

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


@bp.route('/bitrix/admin/1c_exchange.php', methods=['GET', 'POST'])
@auth.login_required
def exchange():
    return base.router(request.args, request.data)
