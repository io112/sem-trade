from flask import request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from app.constants import *
from app.crm import base
from app import app
from werkzeug.security import check_password_hash
from app.core.sessions import *
import json

auth = HTTPBasicAuth()


def check_sid(sid):
    if sid is None:
        return False
    elif not check_session(sid):
        return False
    return True


@auth.verify_password
def verify_password(username, password):
    if username == site_login and \
            check_password_hash(site_password, password):
        return username


@app.route('/', methods=['GET'])
def home():
    sid = request.args.get('sid')
    cs = check_sid(sid)
    if not cs:
        redirect(url_for('home', sid=start_session().get_id()))
    return render_template('create_order/create_order.html')


@app.route('/api/update_session', methods=['POST'])
def update_session_view():
    sid = request.form.get('sid')
    cs = check_sid(sid)
    if not cs:
        return 'fail', 403
    data = json.loads(request.form.get('data', {}))
    session = get_session(sid)
    session.add_data(data)
    update_session(session)
    return 'success'


@app.route('/bitrix/admin/1c_exchange.php', methods=['GET', 'POST'])
@auth.login_required
def exchange():
    return base.router(request.args, request.data)
