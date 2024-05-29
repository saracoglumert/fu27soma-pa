CREATE DATABASE %db_name%;

CREATE TABLE %db_name%.Nodes (
    NodeID int,
    NodeName varchar(255),
    NodeType varchar(255),
    NodeIP varchar(255),
    NodePortUI varchar(255),
    NodePortIndy varchar(255),
    NodePortAries1 varchar(255),
    NodePortAries2 varchar(255),
    DID varchar(255),
    SchemaID varchar(255),
    CredDefID varchar(255),
    ConnectionID varchar(255),
    PRIMARY KEY (NodeID)
);

CREATE TABLE %db_name%.Notifications (
    NotificationID int AUTO_INCREMENT,
    NodeID int,
    NotificationContent varchar(255),
    PRIMARY KEY (NotificationID),
    FOREIGN KEY (NodeID) REFERENCES Nodes(NodeID)
);

CREATE TABLE %db_name%.Products (
    ProductID int,
    ProductName varchar(255),
    PCF varchar(255),
    NodeID int,
    PRIMARY KEY (ProductID),
    FOREIGN KEY (NodeID) REFERENCES Nodes(NodeID)
);

INSERT INTO %db_name%.Nodes (NodeID, NodeName, NodeType, NodeIP, NodePortUI, NodePortIndy, NodePortAries1, NodePortAries2, DID, SchemaID, CredDefID, ConnectionID) VALUES 
(%server_id%, "%server_name%","server","%server_ip%","%server_ui_port%","%server_ledger_port%","%server_acapy_port_1%","%server_acapy_port_2%","N/A","N/A","N/A","N/A"),
(%node1_id%, "%node1_name%","company","%node1_ip%","%node1_ui_port%","N/A","%node1_acapy_port_1%","%node1_acapy_port_2%","N/A","N/A","N/A","N/A"),
(%node2_id%, "%node2_name%","company","%node2_ip%","%node2_ui_port%","N/A","%node2_acapy_port_1%","%node1_acapy_port_2%","N/A","N/A","N/A","N/A");

INSERT INTO %db_name%.Products (ProductID, ProductName, PCF, NodeID) VALUES
(%node1_id%1, "Product A1", "TestPCF-A1",%node1_id%),
(%node1_id%2, "Product A2", "TestPCF-A2",%node1_id%),
(%node2_id%1, "Product B1", "TestPCF-B1",%node2_id%),
(%node2_id%2, "Product B2", "TestPCF-B2",%node2_id%);
