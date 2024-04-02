from flask import Blueprint, render_template

coordinator_bp = Blueprint('coordinator', __name__,
                           template_folder='templates'
                           )
employee_bp = Blueprint('employee', __name__)

from app.routes import coordinator_routes, employee_routes
