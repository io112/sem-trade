from flask_login import current_user
from flask_restful import url_for

from app.constants import commit_hash
from app.views.frontend.base import BaseAuthView


class OrdersView(BaseAuthView):
    template_name = 'orders.html'

    def __init__(self):
        self.api_urls = {
            "API_ORDERS_GET": url_for('orders_api.Orders'.lower()),
            "ORDER_VIEW": '/order/',
        }

    # @orders.route('/', methods=['GET'])
    # @login_required
    # @redirect_restore_pass
    def dispatch_request(self):
        context = {
            'user': current_user,
            'commit_hash': commit_hash
        }
        return self.render_template(context)
