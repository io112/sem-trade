from flask_login import current_user

from app.constants import commit_hash
from app.views.frontend.base import BaseAuthView


class CartsView(BaseAuthView):
    template_name = 'incompleted_orders.html'

    def dispatch_request(self):
        context = {
            'user': current_user,
            'commit_hash': commit_hash
        }
        return self.render_template(context)
