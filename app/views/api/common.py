import flask_restful
from flask_login import login_required


class ApiResource(flask_restful.Resource):
    method_decorators = [login_required]
