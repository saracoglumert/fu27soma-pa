CREATE DATABASE Node1;
CREATE DATABASE Node2;

CREATE TABLE Node1.Products (
    ProductID int,
    ProductName varchar(255),
    Parts varchar(255)
);

CREATE TABLE Node1.Parts (
    PartID int,
    PartName varchar(255),
    PartProducer varchar(255)
);

CREATE TABLE Node2.Products (
    ProductID int,
    ProductName varchar(255),
    Parts varchar(255)
);

CREATE TABLE Node2.Parts (
    PartID int,
    PartName varchar(255),
    PartProducer varchar(255)
);

INSERT INTO Node1.Parts (PartID, PartName, PartProducer)
VALUES (1, "Product 1 - Part 1", "Node2");
VALUES (2, "Product 1 - Part 2", "Node2");

INSERT INTO Node1.Products (ProductID, ProductName, Parts)
VALUES (1,"Product 1","1,2");

INSERT INTO Node2.Parts (PartID, PartName, PartProducer)
VALUES (1, "Product 2 - Part 1", "Node1");
VALUES (2, "Product 2 - Part 2", "Node1");

INSERT INTO Node2.Products (ProductID, ProductName, Parts)
VALUES (1,"Product 2","1,2");
