from flask_login import current_user
from flask_restful.reqparse import RequestParser

from app.constants import commit_hash
from app.core.controllers import order_controller
from app.views.frontend.base import BaseAuthView


class OrdersView(BaseAuthView):
    template_name = 'orders.html'

    # @orders.route('/', methods=['GET'])
    # @login_required
    # @redirect_restore_pass
    def dispatch_request(self):
        context = {
            'user': current_user,
            'commit_hash': commit_hash
        }
        return self.render_template(context)

