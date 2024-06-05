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
    Connections varchar(255),
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
    ProductDescription varchar(255),
    PCFDataExchange TEXT,
    NodeID int,
    CredentialID varchar(255),
    PRIMARY KEY (ProductID),
    FOREIGN KEY (NodeID) REFERENCES Nodes(NodeID)
);

INSERT INTO %db_name%.Nodes (NodeID, NodeName, NodeType, NodeIP, NodePortUI, NodePortIndy, NodePortAries1, NodePortAries2, DID, SchemaID, CredDefID, Connections) VALUES 
(%server_id%, "%server_name%","server","%server_ip%","%server_ui_port%","%server_ledger_port%","%server_acapy_port_1%","%server_acapy_port_2%","N/A","N/A","N/A","[]"),
(%node1_id%, "%node1_name%","client","%node1_ip%","%node1_ui_port%","N/A","%node1_acapy_port_1%","%node1_acapy_port_2%","N/A","N/A","N/A","[]"),
(%node2_id%, "%node2_name%","client","%node2_ip%","%node2_ui_port%","N/A","%node2_acapy_port_1%","%node1_acapy_port_2%","N/A","N/A","N/A","[]");