from flask import Blueprint
from flask_restful import Api

from app.views.api.contragent.contragent_resoure import Contragent, FindContragent

bp = Blueprint('contragent_api', __name__)
api = Api(bp)

api.add_resource(Contragent, '/')
api.add_resource(FindContragent, '/find')
