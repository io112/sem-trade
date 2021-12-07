from flask_restful.reqparse import RequestParser

from app.misc import sid_required
from app.views.api.common import ApiResource


class MakeOrderBase(ApiResource):
    method_decorators = [sid_required]

    CURRENT_ORDER_COOKIE = 'current_order'

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument(self.CURRENT_ORDER_COOKIE, location='cookies', required=True)

