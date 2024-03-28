-- Table: Items
CREATE TABLE Items (
    ItemID INT PRIMARY KEY,
    ItemGroup VARCHAR(255) NOT NULL,
    UnitOfMeasurement VARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(255) NOT NULL,
    StorageLocation VARCHAR(255),
    ContactPerson TEXT,
    PhotoFilePath VARCHAR(255)
);

-- Table: TMARequests
CREATE TABLE TMARequests (
    RequestID INT PRIMARY KEY,
    EmployeeName VARCHAR(255) NOT NULL,
    ItemID INT NOT NULL,
    UnitOfMeasurement VARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    Comment TEXT,
    Status VARCHAR(255) DEFAULT 'New',
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

-- Table: TMARequestRows
CREATE TABLE TMARequestRows (
    RequestID INT NOT NULL,
    RequestRowID INT NOT NULL,
    ItemID INT NOT NULL,
    UnitOfMeasurement VARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    PriceWithoutVAT DECIMAL(10, 2) NOT NULL,
    Comment TEXT,
    PRIMARY KEY (RequestID, RequestRowID),
    FOREIGN KEY (RequestID) REFERENCES TMARequests(RequestID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);