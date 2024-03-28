from flask import Blueprint

coordinator_bp = Blueprint('coordinator', __name__)
employee_bp = Blueprint('employee', __name__)

from app.routes import coordinator_routes, employee_routes
