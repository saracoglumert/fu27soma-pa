DROP DATABASE IF EXISTS %db_name%;
CREATE DATABASE %db_name%;

CREATE TABLE %db_name%.Nodes (
    `nodeID` int AUTO_INCREMENT,
    `nodeName` varchar(255),
    `nodeType` varchar(255),
    `nodeIP` varchar(255),
    `endpoints` varchar(255),
    `did` varchar(255),
    `connections` varchar(255),
    `schemaID` varchar(255),
    `credDefID` varchar(255),
    PRIMARY KEY (NodeID)
);

CREATE TABLE %db_name%.Products (
    `productID` int AUTO_INCREMENT,
    `productName` varchar(255),
    `productDescription` varchar(255),
    `nodeID` INT,
    `status` varchar(255),
    `created` varchar(255),
    `version` varchar(255),
    `data` TEXT,
    `credID` varchar(255),
    `JWT` TEXT,
    PRIMARY KEY (`productID`),
    FOREIGN KEY (`nodeID`) REFERENCES Nodes(`nodeID`)
);

INSERT INTO %db_name%.Nodes (nodeID,nodeName,nodeType,nodeIP,endpoints) VALUES 
(%server_id%, "%server_name%","server","%server_ip%", '{"ui":%server_ui_port%,"indy":%server_ledger_port%,"aries1":%server_acapy_port_1%,"aries2":%server_acapy_port_2%}'),
(%node1_id%, "%node1_name%","client","%node1_ip%", '{"ui":%node1_ui_port%,"aries1":%node1_acapy_port_1%,"aries2":%node1_acapy_port_2%}'),
(%node2_id%, "%node2_name%","client","%node2_ip%", '{"ui":%node2_ui_port%,"aries1":%node2_acapy_port_1%,"aries2":%node2_acapy_port_2%}')