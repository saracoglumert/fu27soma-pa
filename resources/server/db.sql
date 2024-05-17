CREATE DATABASE %db_name%;

CREATE TABLE %db_name%.Nodes (
    NodeID int,
    NodeName varchar(255),
    NodeType varchar(255),
    NodeIP varchar(255),
    NodePortUI varchar(255),
    NodePortAcaPy varchar(255),
    PRIMARY KEY (NodeID)
);

CREATE TABLE %db_name%.Products (
    ProductID int,
    ProductName varchar(255),
    PCF varchar(255),
    NodeID int,
    PRIMARY KEY (ProductID),
    FOREIGN KEY (NodeID) REFERENCES Nodes(NodeID)
);

INSERT INTO %db_name%.Nodes (NodeID, NodeName, NodeType, NodeIP, NodePortUI, NodePortAcaPy) VALUES 
(%server_id%, "%server_name%","server","%server_ip%","%server_ui_port%","%server_acapy_port%"),
(%node1_id%, "%node1_name%","company","%node1_ip%","%node1_ui_port%","%node1_acapy_port_2%"),
(%node2_id%, "%node2_name%","company","%node2_ip%","%node2_ui_port%","%node2_acapy_port_2%");

INSERT INTO %db_name%.Products (ProductID, ProductName, PCF, NodeID) VALUES
(%node1_id%1, "Product A1", "TestPCF-A1",%node1_id%),
(%node1_id%2, "Product A2", "TestPCF-A2",%node1_id%),
(%node2_id%1, "Product B1", "TestPCF-B1",%node2_id%),
(%node2_id%2, "Product B2", "TestPCF-B2",%node2_id%);
