CREATE DATABASE node1;
CREATE DATABASE node2;

CREATE TABLE node1.products (
    ProductID int,
    ProductName varchar(255),
    ProductDesc varchar(255),
    Parts varchar(255)
);

CREATE TABLE node1.parts (
    PartID int,
    PartName varchar(255),
    PartDesc varchar(255),
    PartProducer varchar(255)
);

CREATE TABLE node2.products (
    ProductID int,
    ProductName varchar(255),
    ProductDesc varchar(255),
    Parts varchar(255)
);

CREATE TABLE node2.parts (
    PartID int,
    PartName varchar(255),
    PartDesc varchar(255),
    PartProducer varchar(255)
);


