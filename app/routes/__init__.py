from flask import Blueprint

from app.routes.items import items_bp
from app.routes.requests import requests_bp
from app.routes.general import general_bp

# Create a blueprint for routes
bp = Blueprint('routes', __name__)

# Register the blueprints with the main blueprint
bp.register_blueprint(items_bp)
bp.register_blueprint(requests_bp)
bp.register_blueprint(general_bp)
