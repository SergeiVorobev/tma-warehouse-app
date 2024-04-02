import sqlite3
from sqlite3 import Error

# Create a SQLite database connection
def connect_db():
    conn = None
    try:
        conn = sqlite3.connect('db/database.db')
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn

# Create database tables if they don't exist
def create_tables():
    # Create Items table if it doesn't exist
    with open('db/schema.sql') as f:
        conn = connect_db()
        conn.executescript(f.read())

    cursor = connect_db().cursor()
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
    conn.commit()
    conn.close()
    return cursor
