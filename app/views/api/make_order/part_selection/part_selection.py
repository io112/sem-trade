from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.part_selection.part_selection_resource import PartSearch, PartSubmit, PartPrice

bp = Blueprint('part_selection_api', __name__)

api = Api(bp)

api.add_resource(PartSearch, '/search')
api.add_resource(PartPrice, '/calc')
api.add_resource(PartSubmit, '/submit')
