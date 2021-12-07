import json
import traceback

from flask import request, Response
from flask_restful.reqparse import RequestParser

from app.core.controllers import contragent_controller
from app.views.api.common import ApiResource


class Contragent(ApiResource):
    def post(self):
        data = json.loads(request.form.get('data', []))
        try:
            contragent_controller.create_contragent_from_form(data)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=409)
        return {'success'}


class FindContragent(ApiResource):
    def __init__(self):
        self.find_parser = RequestParser()
        self.find_parser.add_argument('query', type=str, required=True)

    def get(self):
        data = self.find_parser.parse_args()
        return contragent_controller.find_contragents(data['query'])
