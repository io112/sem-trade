from flask import request, render_template
from flask_httpauth import HTTPBasicAuth
from app.constants import *
from app.crm import base
from app import app
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/bitrix/admin/1c_exchange.php', methods=['GET', 'POST'])
@auth.login_required
def exchange():
    return base.router(request.args, request.data)
