import sqlite3
from flask import render_template, current_app
from app.routes import coordinator_bp

@coordinator_bp.route('/goods')
def coordinator_goods():
    conn = sqlite3.connect(current_app.config['SQLALCHEMY_DATABASE_URI'])
    cursor = conn.cursor()
    # Implement logic to fetch and display goods list
    return render_template('coordinator/goods.html')

@coordinator_bp.route('/purchase_requests')
def coordinator_purchase_requests():
    conn = sqlite3.connect(current_app.config['SQLALCHEMY_DATABASE_URI'])
    cursor = conn.cursor()
    # Implement logic to fetch and display purchase requests list
    return render_template('coordinator/purchase_requests.html')
