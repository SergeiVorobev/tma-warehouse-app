from flask import Flask
from app.config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

from app.routes import bp as routes_bp
app.register_blueprint(routes_bp)