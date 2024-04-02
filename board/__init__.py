from flask import Flask
import sqlite3

from board import pages
from .config import Config
from .db import connect_db, create_tables

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    # # Create a SQLite database connection
    # conn = connect_db()
    # conn.row_factory = sqlite3.Row
    # cursor = conn.cursor()

    # Create Items table if it doesn't exist
    # create_tables()
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS Items (
    #         ItemID INTEGER PRIMARY KEY,
    #         ItemGroup VARCHAR(255) NOT NULL,
    #         UnitOfMeasurement VARCHAR(255) NOT NULL,
    #         Quantity INTEGER NOT NULL,
    #         PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    #         Status VARCHAR(255) NOT NULL,
    #         StorageLocation VARCHAR(255),
    #         ContactPerson TEXT,
    #         PhotoFilePath VARCHAR(255)
    #     )
    # """)

    # # Create TMARequests table if it doesn't exist
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS TMARequests (
    #         RequestID INTEGER PRIMARY KEY,
    #         EmployeeName VARCHAR(255) NOT NULL,
    #         ItemID INTEGER NOT NULL,
    #         UnitOfMeasurement VARCHAR(255) NOT NULL,
    #         Quantity INTEGER NOT NULL,
    #         PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    #         Comment TEXT,
    #         Status VARCHAR(255) DEFAULT 'New',
    #         FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
    #     )
    # """)

    # # Create TMARequestRows table if it doesn't exist
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS TMARequestRows (
    #         RequestID INTEGER NOT NULL,
    #         RequestRowID INTEGER NOT NULL,
    #         ItemID INTEGER NOT NULL,
    #         UnitOfMeasurement VARCHAR(255) NOT NULL,
    #         Quantity INTEGER NOT NULL,
    #         PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    #         Comment TEXT,
    #         PRIMARY KEY (RequestID, RequestRowID),
    #         FOREIGN KEY (RequestID) REFERENCES TMARequests(RequestID),
    #         FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
    #     )
    # """)

    app.register_blueprint(pages.bp)
    app.register_blueprint(pages.coordinator_bp)
    app.register_blueprint(pages.employee_bp)
    return app