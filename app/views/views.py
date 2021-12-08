from app import app
from app.views.api.api import api
from app.views.frontend.frontend import frontend

app.register_blueprint(frontend, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')
