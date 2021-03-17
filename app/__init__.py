from flask import Flask
from flask_login import LoginManager

from app.db import init
from app import constants

app = Flask(__name__)
app.config['SECRET_KEY'] = constants.secret_key
login_manager = LoginManager()
login_manager.init_app(app)

from app import views

if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0')
