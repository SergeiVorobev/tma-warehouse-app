DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS TMARequests;
DROP TABLE IF EXISTS TMARequestRows;

CREATE TABLE Items (
    ItemID INTEGER PRIMARY KEY,
    ItemGroup VARCHAR(255) NOT NULL,
    UnitOfMeasurement VARCHAR(255) NOT NULL,
    Quantity INTEGER NOT NULL,
    PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(255) NOT NULL,
    StorageLocation VARCHAR(255),
    ContactPerson TEXT,
    PhotoFilePath VARCHAR(255)
);
 CREATE TABLE TMARequests (
    RequestID INTEGER PRIMARY KEY,
    EmployeeName VARCHAR(255) NOT NULL,
    ItemID INTEGER NOT NULL,
    UnitOfMeasurement VARCHAR(255) NOT NULL,
    Quantity INTEGER NOT NULL,
    PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    Comment TEXT,
    Status VARCHAR(255) DEFAULT 'New',
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);
 CREATE TABLE TMARequestRows (
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
);