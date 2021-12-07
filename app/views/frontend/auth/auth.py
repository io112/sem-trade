from flask import request, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.constants import commit_hash
from app.core.controllers import users_controller
from app.core.models.user import User
from app.views.frontend.base import BaseAuthView, BaseView


class LoginView(BaseView):
    methods = ['GET', 'POST']
    template_name = 'login.html'

    def dispatch_request(self):
        context = {
            'commit_hash': commit_hash
        }

        if request.method == 'POST':
            if current_user.is_authenticated:
                return redirect(url_for('frontend.create_order.create_order'))
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.get_by_username(username)
            user: User
            if user is not None and user.check_password(password):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('frontend.create_order.create_order')
                return redirect(next_page)
        elif current_user.is_authenticated:
            return redirect(url_for('frontend.create_order.create_order'))
        return self.render_template(context)


class LogoutView(BaseAuthView):
    def dispatch_request(self):
        logout_user()
        return redirect(url_for('frontend.create_order.create_order'))


class ChangePasswordView(BaseAuthView):
    methods = ['POST', 'GET']
    template_name = 'login_change_password.html'

    def dispatch_request(self):
        if request.method == 'POST':
            try:
                users_controller.change_password(user=current_user, **request.form)
            except Exception as e:
                print(e.args)
                return render_template('login_change_password.html',
                                       error=str(e), user=current_user,
                                       commit_hash=commit_hash)

        if not current_user.change_password:
            return redirect(url_for('frontend.create_order.create_order'))
        return render_template('login_change_password.html', user=current_user, commit_hash=commit_hash)
