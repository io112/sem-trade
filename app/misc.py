import functools
import random
import string

from flask import make_response, redirect, url_for, request
from flask_login import current_user

from app.core.controllers import session_controller
from app.core.sessions import check_session, start_session


def check_sid(sid):
    if sid is None:
        return False
    elif not check_session(sid):
        return False
    elif session_controller.get_session(sid).user != current_user.username:
        return False
    return True


def make_cookie_resp(url, sid=None):
    if sid:
        resp = make_response(redirect(url_for(url)))
        resp.set_cookie('current_order', sid)
    else:
        session = start_session(current_user.username)
        resp = make_response(redirect(url_for(url)))
        resp.set_cookie('current_order', session.id)
    return resp


def sid_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        sid = request.args.get('sid', None)
        if sid is not None:
            cs = check_sid(sid)
            if cs:
                resp = make_cookie_resp('frontend.create_order.create_order', sid)
            else:
                resp = make_cookie_resp('frontend.create_order.create_order')
            return resp
        sid = request.cookies.get('current_order')
        if not check_sid(sid):
            return make_cookie_resp('frontend.create_order.create_order')
        return view(**kwargs)

    return wrapped_view


def redirect_restore_pass(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.change_password:
            return redirect(url_for('login_change_pass'))
        return view(**kwargs)

    return wrapped_view
