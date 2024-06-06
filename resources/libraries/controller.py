import mysql.connector
import requests
import json
import random
import string
import time
from redis import Redis
import ast
import pprint
import sys

conn_db = mysql.connector.connect(
  host="10.10.10.200",
  user="root",
  password="12345",
  database="fu27soma",
  autocommit=True)

conn_redis = Redis.from_url(url="redis://10.10.10.200:7000")

def getServerID():
    cursor = conn_db.cursor()
    cursor.execute("SELECT NodeID FROM Nodes WHERE nodeType='server'")
    result = cursor.fetchone()[0]
    
    return result

class Node:
    def __init__(self,id):
        self.id = id
        self.update()

    def update(self):
        cursor = conn_db.cursor()
        cursor.execute("SELECT * FROM Nodes WHERE nodeID = {}".format(self.id))
        result = cursor.fetchone()

        self.id = result[0]
        self.name = result[1]
        self.type = result[2]
        self.ip = result[3]
        self.endpoints = json.loads(result[4])
        self.did = result[5]
        
        if result[6] == None:
            self.connections = json.loads("{}")
        else:
            self.connections = json.loads(result[6])

        for key,value in self.endpoints.items():
            self.endpoints[key] = "http://{}:{}".format(self.ip,value)

        if self.type == "server":
            self.schemaid = result[7]
            self.creddefid = result[8]

    def register(self):
        # Create DID from seed
        body = json.loads('{"method": "sov","options": {"key_type": "ed25519"},"seed": "#"}'.replace("#",''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))))
        r=requests.post(url = self.endpoints["aries2"]+'/wallet/did/create', json=body)
        did = json.loads(r.content)['result']['did']
        verkey = json.loads(r.content)['result']['verkey']

        # Register DID into ledger
        body = json.loads('{"role":"ENDORSER","alias":null,"did":"#","verkey":"%"}'.replace("#",did).replace("%",verkey))
        r = requests.post(url = Node(getServerID()).endpoints["indy"]+"/register", json = body)
        did = json.loads(r.content)['did']

        # Publish DID
        r=requests.post(url = self.endpoints["aries2"]+'/wallet/did/public?did={}'.format(did), json=body)
    
        # Register into DB
        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET did = '{}' WHERE nodeID = {}".format(did,self.id)
        cursor.execute(sql)
        conn_db.commit()

        if self.type == "server":
            # Register Schema
            #{"specVersion": "ver1", "version": "ver1", "created": 1717371325, "status": "Active", "companyName": "Siemens", "companyIds": 201, "productDescription": "descp1", "productIds": "101", "productCategoryCpc": "cpc1", "productNameCompany": "name1", "comment": "comment1", "pcf": "pcf1"}
            body = json.loads('{"attributes": ["data"],"schema_name": "data","schema_version": "1.0"}')
            r=requests.post(url = self.endpoints["aries2"]+'/schemas', json=body)
            schema_id = json.loads(r.content)['sent']['schema_id']

            # Register into DB
            cursor = conn_db.cursor()
            sql = "UPDATE Nodes SET schemaID = '{}' WHERE nodeID={}".format(schema_id,self.id)
            cursor.execute(sql)
            conn_db.commit()

            # Regsiter Credential Definition
            cursor = conn_db.cursor()
            cursor.execute("SELECT schemaID FROM Nodes WHERE nodeID={}".format(self.id))
            schema_id = cursor.fetchone()[0]

            #cred def revocation
            body = json.loads('{"schema_id": "#","support_revocation": false,"tag": "default"}'.replace("#",schema_id))
            #body = json.loads('{"revocation_registry_size": 1000,"schema_id": "#","support_revocation": true,"tag": "default"}'.replace("#",schema_id))
            r=requests.post(url = self.endpoints["aries2"]+'/credential-definitions', json=body)
            credential_definition_id = json.loads(r.content)['sent']['credential_definition_id']

            # Register into DB
            cursor = conn_db.cursor()
            sql = "UPDATE Nodes SET credDefID = '{}' WHERE nodeID={}".format(credential_definition_id,self.id)
            cursor.execute(sql)
            conn_db.commit()

        elif self.type == "client":
            self.connect(getServerID())

    def connect(self,id):
        target = Node(id)
        
        # Step 1 - Create Invitation (node2 - faber)
        body = json.loads('{"service_endpoint": "#"}'.replace("#",target.endpoints["aries1"]))
        r=requests.post(url = target.endpoints["aries2"]+'/connections/create-invitation', json=body)
        cid = json.loads(r.content)['invitation']['@id']
        response1 = json.dumps((json.loads(r.content)['invitation']), sort_keys=True, indent=4)
        time.sleep(1.5)

        # Step 2 - Receive Invitation (node1 - alice)
        body = response1
        r=requests.post(url = self.endpoints["aries2"]+'/connections/receive-invitation', json=body)
        cid = json.loads(r.content)['connection_id']
        response2 = json.loads(r.content)['connection_id']
        time.sleep(1.5)

        # Step 3 - Accept Invitation (node1 - alice)
        x = self.endpoints["aries2"]+'/connections/{}/accept-invitation?my_endpoint={}'.format(response2,self.endpoints["aries1"])
        r=requests.post(url = x)
        response3 = json.loads(r.content)
        time.sleep(1.5)

        # Step 4 - Accept Request (node2 - faber)
        response4 = json.loads(conn_redis.lrange(str.encode('acapy-record-with-state-base'), -1, -1)[0].decode("utf-8"))['payload']['payload']['connection_id']
        x = target.endpoints["aries2"]+'/connections/{}/accept-request?my_endpoint={}'.format(response4,target.endpoints["aries1"])
        r=requests.post(url = x)
        response5 = r.content
        time.sleep(1.5)

        # Register into DB - Node 1
        cursor = conn_db.cursor()
        cursor.execute("SELECT connections FROM Nodes WHERE nodeID = {}".format(self.id))
        result = cursor.fetchone()[0]

        if result == None:
            data = {}
            data[id] = response2
            data = json.dumps(data)
        else:
            data = json.loads(result)
            data[id] = response2
            data = json.dumps(data)
        

        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET connections = '{}' WHERE nodeID={}".format(data,self.id)
        cursor.execute(sql)
        conn_db.commit()

        # Register into DB - Node 2
        cursor = conn_db.cursor()
        cursor.execute("SELECT connections FROM Nodes WHERE nodeID = {}".format(id))
        result = cursor.fetchone()[0]

        if result == None:
            data = {}
            data[self.id] = response4
            data = json.dumps(data)
        else:
            data = json.loads(result)
            data[self.id] = response4
            data = json.dumps(data)
        

        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET connections = '{}' WHERE nodeID={}".format(data,id)
        cursor.execute(sql)
        conn_db.commit()

class Server(Node):
    def __init__(self,id):
        super().__init__(id)
    
    def getProducts(self):
        cursor = conn_db.cursor()
        cursor.execute("SELECT * FROM Products".format(self.id))
        return [list(i) for i in list(cursor.fetchall())]
    
    def IssueCredential(self,product):
        cursor = conn_db.cursor()
        cursor.execute("SELECT * FROM Products WHERE productID={}".format(product))
        temp = cursor.fetchall()[0]
        
        print("Issue credential for: {}".format(temp))

        connectionid = self.connections['{}'.format(temp[3])]

        body = """
            {
            "auto_issue": true,
            "auto_remove": true,
            "auto_offer": true,
            "connection_id": "$",
            "credential_preview": {
                "@type": "issue-credential/2.0/credential-preview",
                "attributes": [
                {"name": "data", "value": "$$"}
                ]
            },
            "filter": {
                "indy": {
                "cred_def_id": "#1#"
                }
            },
            "trace": true
            }
        """

        body = body.replace("$",connectionid)
        body = body.replace("#1#",self.creddefid)
        body = body.replace("$$",temp[7])
        r=requests.post(url = self.endpoints["aries2"]+'/issue-credential-2.0/send', json=json.loads(body))
        
        response1 = json.loads(r.content)['cred_ex_id']
        time.sleep(1.5)
        response2 = json.loads(conn_redis.lrange(str.encode('acapy-record-with-state-base'), -1, -1)[0].decode("utf-8"))['payload']['payload']['cred_ex_id']

        # send request to 201 /cred_ex/send-request with response 2
        r = requests.post(url = Client(int(temp[3])).endpoints["aries2"]+'/issue-credential-2.0/records/{}/send-request'.format(response2))
        # burdan sonra response 2 ile storela
        time.sleep(1.5)
        # send request to 201 /store with reponse 2
        r = requests.post(url = Client(int(temp[3])).endpoints["aries2"]+'/issue-credential-2.0/records/{}/store'.format(response2),data=json.loads('{"credential_id": "%"}'.replace("%",temp[1])))
        response5 = r.content
        credid = json.loads(response5)['indy']['cred_id_stored']

        cursor = conn_db.cursor()
        sql = "UPDATE Products SET credID = '{}' WHERE productID = {}".format(credid,temp[0])
        cursor.execute(sql)
        conn_db.commit()
       
    
class Client(Node):
    def __init__(self,id):
        super().__init__(id)
    
    def scCompanies(self):
        cursor = conn_db.cursor()
        cursor.execute("SELECT * FROM Nodes WHERE nodeID!={} AND nodeID!={}".format(self.id,getServerID()))
        return [list(i) for i in list(cursor.fetchall())]
    
    def scProducts(self):
        cursor = conn_db.cursor()
        cursor.execute("SELECT * FROM Products WHERE nodeID!={} AND credID IS NOT NULL".format(self.id))
        temp = []
        for element in list(cursor.fetchall()):
            if '{}'.format(element[3]) in list(self.connections.keys()):
                temp.append(element)
        return temp
        
    def getProducts(self):
        cursor = conn_db.cursor()
        cursor.execute("SELECT * FROM Products WHERE nodeID = {}".format(self.id))
        return [list(i) for i in list(cursor.fetchall())]
            
    def newProduct(self,name,description,version,data):        
        cursor = conn_db.cursor()
        sql = "INSERT INTO Products (productName, productDescription, nodeID, status, created, version, data) VALUES ('{}', '{}', {}, '{}', '{}', '{}', '{}')".format(name,description,self.id,"active",round(time.time()),version,data)
        cursor.execute(sql)
        conn_db.commit()