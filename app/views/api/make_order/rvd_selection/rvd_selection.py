from flask import Blueprint
from flask_restful import Api

from app.views.api.make_order.rvd_selection.rvd_selection_resource import MakeOrderSelection, SelectionPartSearch, \
    SelectionPartCalcPrice, SelectionJobType, SelectionAmount, SelectionSubmit

bp = Blueprint('rvd_selection_api', __name__)

api = Api(bp)
api.add_resource(MakeOrderSelection, '/')
api.add_resource(SelectionPartSearch, '/part/search')
api.add_resource(SelectionPartCalcPrice, '/part/calc')
api.add_resource(SelectionJobType, '/job')
api.add_resource(SelectionAmount, '/amount')
api.add_resource(SelectionSubmit, '/submit')
