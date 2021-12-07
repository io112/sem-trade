from flask import url_for as flask_url_for
from flask_restful import url_for
from flask_login import current_user

from app.constants import commit_hash
from app.misc import sid_required
from app.views.frontend.base import BaseAuthView


class CreateOrderView(BaseAuthView):
    decorators = [sid_required]
    template_name = 'create_order/create_order.html'

    def __init__(self):
        self.api_urls = {
            'API_SELECTION_PART_ADD': url_for('rvd_selection_api.MakeOrderSelection'.lower()),
            'API_SELECTION_PART_DEL': url_for('rvd_selection_api.MakeOrderSelection'.lower()),
            'API_SELECTION_PART_CALC': url_for('rvd_selection_api.SelectionPartCalcPrice'.lower()),
            'API_SELECTION_PART_SEARCH': url_for('rvd_selection_api.SelectionPartSearch'.lower()),
            'API_SELECTION_JOB_SET': url_for('rvd_selection_api.SelectionJobType'.lower()),
            'API_SELECTION_UPDATE': url_for('rvd_selection_api.MakeOrderSelection'.lower()),
            'API_SELECTION_AMOUNT_UPDATE': url_for('rvd_selection_api.SelectionAmount'.lower()),
            'API_SELECTION_SUBMIT': url_for('rvd_selection_api.SelectionSubmit'.lower()),
            'API_CART_GET': url_for('order_cart_api.OrderCart'.lower()),
            'API_CART_DEL': url_for('order_cart_api.OrderCart'.lower()),
            'API_CHECKOUT': url_for('order_checkout_api.OrderCheckout'.lower()),
            'API_CONTRAGENT_GET': url_for('order_contragent_api.OrderContragent'.lower()),
            'API_CONTRAGENT_SET': url_for('order_contragent_api.OrderContragent'.lower()),
            'API_CONTRAGENT_DEL': url_for('order_contragent_api.OrderContragent'.lower()),
            'API_CONTRAGENT_FIND': url_for('contragent_api.FindContragent'.lower()),
            'API_PART_SEARCH': url_for('part_selection_api.PartSearch'.lower()),
            'API_PART_CALC': url_for('part_selection_api.PartPrice'.lower()),
            'API_PART_SUBMIT': url_for('part_selection_api.PartSubmit'.lower()),
            'API_SERVICE_SUBMIT': url_for('service_selection_api.SubmitService'.lower()),
            'API_COMMENT_SET': url_for('order_comment_api.OrderComment'.lower()),
            'API_COMMENT_GET': url_for('order_comment_api.OrderComment'.lower()),
            'API_CARTS_GET': url_for('order_carts_api.OrderCarts'.lower()),
        }

    def dispatch_request(self):
        context = {
            'user': current_user,
            'commit_hash': commit_hash
        }
        return self.render_template(context)
