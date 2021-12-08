from flask import render_template
from flask_login import current_user

from app.constants import commit_hash
from app.views.frontend.base import BaseAuthView


class CreateUserView(BaseAuthView):
    template_name = 'create_user.html'

    def dispatch_request(self):
        context = {
            'user': current_user,
            'commit_hash': commit_hash
        }
        return self.render_template(context)
