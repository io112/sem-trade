from flask import Flask
from flask_login import LoginManager

from app import db
from app import constants

app = Flask(__name__)
app.config['SECRET_KEY'] = constants.secret_key
login_manager = LoginManager()
login_manager.init_app(app)

from app import base_views, api_views

db.init()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=constants.internal_port)
