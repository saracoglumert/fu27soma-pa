import mysql.connector
import requests
import json
import random
import string
import time
from redis import Redis

db = mysql.connector.connect(
  host="10.10.10.200",
  user="root",
  password="12345",
  database="fu27soma")

class Notifications:
    def __init__(self,node):
        self.node = node
        
    def New(self,content):
        cursor = db.cursor()
        sql = "INSERT INTO Notifications (NodeID, NotificationContent) VALUES ({}, '{}')".format(self.node,content)
        cursor.execute(sql)
        db.commit()

class Product:
    def __init__(self,id):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Products WHERE ProductID = {}".format(id))
            result = cursor.fetchone()
                    
            self.id = result[0]
            self.name = result[1]
            self.pcf = result[2]
            self.company = result[3]
        except Exception as e:
            print(str(e))

    def ProducttoList(self):
        return [self.id,self.name,self.pcf,self.company]

class Node:
    def __init__(self, id):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Nodes WHERE NodeID = {}".format(id))
            result1 = cursor.fetchone()
            cursor.execute("SELECT ProductID FROM Products WHERE NodeID = {}".format(id))
            result2 = [i[0] for i in cursor.fetchall()]
            result3 = []
            for id in result2:
                result3.append(Product(id))

            self.id = result1[0]
            self.name = result1[1]
            self.type = result1[2]
            self.ip = result1[3]
            self.port_ui = result1[4]
            self.port_indy = result1[5]
            self.port_acapy1 = result1[6]
            self.port_acapy2 = result1[7]
            self.endpoint_ui = "http://{}:{}".format(result1[3],result1[4])
            self.endpoint_acapy1 = "http://{}:{}".format(result1[3],result1[6])
            self.endpoint_acapy2 = "http://{}:{}".format(result1[3],result1[7])
            self.did = result1[8]
            self.schemaid = result1[9]
            self.creddefid = result1[10]
            self.connectionid = result1[11]
            self.products = result3
        except Exception as e:
            print(str(e))
    
    def ProductstoList(self):
        temp = []
        for element in self.products:
            temp.append([element.id,element.name,element.pcf,element.company])
        return temp

    def RegisterDID(self):
        # Create DID from seed
        body = json.loads('{"method": "sov","options": {"key_type": "ed25519"},"seed": "#"}'.replace("#",''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))))
        r=requests.post(url = self.endpoint_acapy2+'/wallet/did/create', json=body)
        did = json.loads(r.content)['result']['did']
        verkey = json.loads(r.content)['result']['verkey']

        # Register DID into ledger
        body = json.loads('{"role":"ENDORSER","alias":null,"did":"#","verkey":"%"}'.replace("#",did).replace("%",verkey))
        r = requests.post(url = "http://10.10.10.200:8000/register", json = body)
        did = json.loads(r.content)['did']

        # Publish DID
        r=requests.post(url = self.endpoint_acapy2+'/wallet/did/public?did={}'.format(did), json=body)
    
        # Register into DB
        cursor = db.cursor()
        sql = "UPDATE Nodes SET DID = '{}' WHERE NodeID = {}".format(did,self.id)
        cursor.execute(sql)
        db.commit()

        # Register Notification
        Notifications(self.id).New("DID registered. ({})".format(did))

    def RegisterSchema(self):
        body = json.loads('{"attributes": ["company","product","PCF"],"schema_name": "PCF_Schema","schema_version": "1.0"}')
        r=requests.post(url = self.endpoint_acapy2+'/schemas', json=body)
        schema_id = json.loads(r.content)['sent']['schema_id']

        # Register into DB
        cursor = db.cursor()
        sql = "UPDATE Nodes SET SchemaID = '{}' WHERE NodeID={}".format(schema_id,self.id)
        cursor.execute(sql)
        db.commit()

        # Register Notification
        Notifications(self.id).New("Schema registered. ({})".format(schema_id))

    def RegisterCredentialDefinition(self):
        cursor = db.cursor()
        cursor.execute("SELECT SchemaID FROM Nodes WHERE NodeID={}".format(self.id))
        schema_id = cursor.fetchone()[0]

        body = json.loads('{"revocation_registry_size": 1000,"schema_id": "#","support_revocation": true,"tag": "default"}'.replace("#",schema_id))
        r=requests.post(url = self.endpoint_acapy2+'/credential-definitions', json=body)
        credential_definition_id = json.loads(r.content)['sent']['credential_definition_id']

        # Register into DB
        cursor = db.cursor()
        sql = "UPDATE Nodes SET CredDefID = '{}' WHERE NodeID={}".format(credential_definition_id,self.id)
        cursor.execute(sql)
        db.commit()

        # Register Notification
        Notifications(self.id).New("Credential definiton registered. ({})".format(credential_definition_id))

    def Connect(self,id):
        rds = Redis.from_url(url="redis://10.10.10.200:7000")
        
        # Step 1 - Create Invitation (node2 - faber)
        body = json.loads('{"service_endpoint": "#"}'.replace("#",Node(id).endpoint_acapy1))
        r=requests.post(url = Node(id).endpoint_acapy2+'/connections/create-invitation', json=body)
        cid = json.loads(r.content)['invitation']['@id']
        response1 = json.dumps((json.loads(r.content)['invitation']), sort_keys=True, indent=4)
        time.sleep(1.5)

        # Step 2 - Receive Invitation (node1 - alice)
        body = response1
        r=requests.post(url = self.endpoint_acapy2+'/connections/receive-invitation', json=body)
        cid = json.loads(r.content)['connection_id']
        response2 = json.loads(r.content)['connection_id']
        time.sleep(1.5)

        # Step 3 - Accept Invitation (node1 - alice)
        x = self.endpoint_acapy2+'/connections/{}/accept-invitation?my_endpoint={}'.format(response2,self.endpoint_acapy1)
        r=requests.post(url = x)
        response3 = json.loads(r.content)
        time.sleep(1.5)

        # Step 4 - Accept Request (node2 - faber)
        response4 = json.loads(rds.lrange(str.encode('acapy-record-with-state-base'), -1, -1)[0].decode("utf-8"))['payload']['payload']['connection_id']
        x = Node(id).endpoint_acapy2+'/connections/{}/accept-request?my_endpoint={}'.format(response4,Node(id).endpoint_acapy1)
        r=requests.post(url = x)
        response5 = r.content
        time.sleep(5)

        # Register into DB - Node 1
        cursor = db.cursor()
        sql = "UPDATE Nodes SET ConnectionID = '{}' WHERE NodeID={}".format(response2,self.id)
        cursor.execute(sql)
        db.commit()

        # Register into DB - Node 2
        cursor = db.cursor()
        sql = "UPDATE Nodes SET ConnectionID = '{}' WHERE NodeID={}".format(response4,id)
        cursor.execute(sql)
        db.commit()

class SupplyChain:
    def __init__(self,id):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT NodeID FROM Nodes WHERE NodeID!={} AND NodeID!={}".format(id,GetServerID()))
            result1 = [i[0] for i in cursor.fetchall()]
            result2 = []
            for id in result1:
                result2.append(Node(id))

            self.companies = result2
        except Exception as e:
            print(str(e))

    def CompaniestoList(self):
        temp = []
        for element in self.companies:
            temp.append([element.id,element.name,element.ip,element.port_ui,element.port_acapy1,element.port_acapy2,element.endpoint_ui,element.products,len(element.products)])
        return temp
    
    def ProductstoList(self):
        temp1 = []
        temp2 = []
        for productsofcompany in self.companies:
            temp1.append(productsofcompany.products)
        for productsofcompany in temp1:
            for product in productsofcompany:
                temp2.append([product.id,product.name,product.pcf,product.company,Node(product.company).name])
        return temp2

def Endpoints():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Nodes")
    results = cursor.fetchall()
    
    temp = []

    for result in results:
        if result[5] == "N/A":
            temp.append([result[0],
                        result[1],
                        result[2],
                        result[3],
                        "http://{}:{}".format(result[3],result[4]),
                        "N/A",
                        "http://{}:{}".format(result[3],result[6]),
                        "http://{}:{}".format(result[3],result[7])])
        else:
            temp.append([result[0],
                        result[1],
                        result[2],
                        result[3],
                        "http://{}:{}".format(result[3],result[4]),
                        "http://{}:{}".format(result[3],result[5]),
                        "http://{}:{}".format(result[3],result[6]),
                        "http://{}:{}".format(result[3],result[7])])

    return temp

def GetServerID():
    cursor = db.cursor()
    cursor.execute("SELECT NodeID FROM Nodes WHERE NodeType='server'")
    result = cursor.fetchone()[0]
    
    return result
