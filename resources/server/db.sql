CREATE DATABASE %db_name%;

CREATE TABLE %db_name%.Companies (
    CompanyID int,
    CompanyName varchar(255),
    CompanyIP varchar(255),
    CompanyPortUI varchar(255),
    CompanyPortAcaPy varchar(255),
    PRIMARY KEY (companyID)
);

CREATE TABLE %db_name%.Products (
    ProductID int,
    ProductName varchar(255),
    PCF varchar(255),
    CompanyID int,
    PRIMARY KEY (ProductID),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);

INSERT INTO %db_name%.Companies (CompanyID, CompanyName, CompanyIP, CompanyPortUI, CompanyPortAcaPy) VALUES 
(%node1_id%, "%node1_name%","%node1_ip%","%node1_ui_port%","%node1_acapy_port_2%"),
(%node2_id%, "%node2_name%","%node2_ip%","%node2_ui_port%","%node2_acapy_port_2%");

INSERT INTO %db_name%.Products (ProductID, ProductName, PCF, CompanyID) VALUES
(%node1_id%1, "Product A1", "TestPCF-A1",%node1_id%),
(%node1_id%2, "Product A2", "TestPCF-A2",%node1_id%),
(%node2_id%1, "Product B1", "TestPCF-B1",%node2_id%),
(%node2_id%2, "Product B2", "TestPCF-B2",%node2_id%);
