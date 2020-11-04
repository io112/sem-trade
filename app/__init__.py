from flask import Flask
from app.db import init

app = Flask(__name__)
init()

from app import views

if __name__ == '__main__':
    app.run(host='0.0.0.0')
