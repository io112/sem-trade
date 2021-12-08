from flask_login import current_user
from flask_restful import url_for

from app.constants import commit_hash
from app.views.frontend.base import BaseAuthView


class CartsView(BaseAuthView):
    template_name = 'carts.html'

    def __init__(self):
        self.api_urls = {
            "API_CARTS_GET": url_for('carts_api.Carts'.lower()),
            "API_CARTS_DELETE": url_for('carts_api.Carts'.lower()),
            "MAKE_ORDER_URL": url_for('frontend.create_order.create_order'.lower()),
        }

    def dispatch_request(self):
        context = {
            'user': current_user,
            'commit_hash': commit_hash
        }
        return self.render_template(context)
