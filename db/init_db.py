import sqlite3

connection = sqlite3.connect('db/database.db')


with open('db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("""
    INSERT INTO Items (ItemGroup, UnitOfMeasurement, Quantity, PriceWithoutVAT, Status, StorageLocation, ContactPerson, PhotoFilePath)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", ("item_group", "unit_of_measurement", "quantity", "price_without_vat", "status", "storage_location", "contact_person", "photo_file_path"))
connection.commit()
connection.close()
