from flask import Flask
import sqlite3

app = Flask(__name__)

# Create a SQLite database connection
conn = sqlite3.connect("tma_warehouse.db")
cursor = conn.cursor()

# Create Items table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Items (
        ItemID INTEGER PRIMARY KEY,
        ItemGroup VARCHAR(255) NOT NULL,
        UnitOfMeasurement VARCHAR(255) NOT NULL,
        Quantity INTEGER NOT NULL,
        PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
        Status VARCHAR(255) NOT NULL,
        StorageLocation VARCHAR(255),
        ContactPerson TEXT,
        PhotoFilePath VARCHAR(255)
    )
""")

# Create TMARequests table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TMARequests (
        RequestID INTEGER PRIMARY KEY,
        EmployeeName VARCHAR(255) NOT NULL,
        ItemID INTEGER NOT NULL,
        UnitOfMeasurement VARCHAR(255) NOT NULL,
        Quantity INTEGER NOT NULL,
        PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
        Comment TEXT,
        Status VARCHAR(255) DEFAULT 'New',
        FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
    )
""")

# Create TMARequestRows table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TMARequestRows (
        RequestID INTEGER NOT NULL,
        RequestRowID INTEGER NOT NULL,
        ItemID INTEGER NOT NULL,
        UnitOfMeasurement VARCHAR(255) NOT NULL,
        Quantity INTEGER NOT NULL,
        PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
        Comment TEXT,
        PRIMARY KEY (RequestID, RequestRowID),
        FOREIGN KEY (RequestID) REFERENCES TMARequests(RequestID),
        FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
    )
""")

conn.commit()

@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)

