from flask import Flask

from run import app
from app.routes import employee_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(employee_bp, url_prefix='/employee')
    return app
