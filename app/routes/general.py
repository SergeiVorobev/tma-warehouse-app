from flask import Blueprint, render_template

general_bp = Blueprint('general_bp', __name__,
    template_folder='templates')

@general_bp.route('/')
def index():
    return render_template('base.html')

@general_bp.route('/about')
def about():
    return render_template('about.html')
