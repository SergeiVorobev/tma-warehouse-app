from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/tma_warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.routes import coordinator_routes, employee_routes

