from flask import render_template
from flask.views import View
from flask_login import login_required

from app.misc import redirect_restore_pass


class BaseAuthView(View):
    template_name = ''
    decorators = [login_required, redirect_restore_pass]
    api_urls = {}

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), api_urls=self.api_urls, **context)

    def dispatch_request(self):
        raise NotImplementedError()


class BaseView(View):
    template_name = ''

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        raise NotImplementedError()
