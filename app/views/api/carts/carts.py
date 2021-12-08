from flask import Blueprint
from flask_restful import Api

from app.views.api.carts.carts_resource import Carts

bp = Blueprint('carts_api', __name__)

api = Api(bp)

api.add_resource(Carts, '/')
