from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.service.service_resource import SubmitService

bp = Blueprint('service_selection_api', __name__)

api = Api(bp)

api.add_resource(SubmitService, '/submit')
