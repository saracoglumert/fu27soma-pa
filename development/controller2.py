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

sys.setrecursionlimit(sys.getrecursionlimit())

conn_db = mysql.connector.connect(
  host="10.10.10.200",
  user="root",
  password="12345",
  database="fu27soma")

conn_redis = Redis.from_url(url="redis://10.10.10.200:7000")

def GetServerID():
    cursor = conn_db.cursor()
    cursor.execute("SELECT NodeID FROM Nodes WHERE NodeType='server'")
    result = cursor.fetchone()[0]
    
    return result

def Notification(id,content):
  cursor = conn_db.cursor()
  sql = "INSERT INTO Notifications (NodeID, NotificationContent) VALUES ({}, '{}')".format(id,content)
  cursor.execute(sql)
  conn_db.commit()

class Product:
    def __init__(self,id):
        try:
            cursor = conn_db.cursor()
            cursor.execute("SELECT * FROM Products WHERE ProductID = {}".format(id))
            result = cursor.fetchone()
                    
            self.id = result[0]
            self.name = result[1]
            self.description = result[2]
            self.pcfdataexchange = result[3]
            self.company = result[4]
            self.credential = result[5]
            self.node = Client(self.company).node
        except Exception as e:
            print("Error :{}".format(str(e)))

    def toList(self):
        return [self.id,self.name,self.pcf,self.company]

    def IssueCredential(self):
        connectionid = Server(GetServerID()).node.connections[self.company]
        body = """
            {
            "auto_remove": true,
            "comment": "string",
            "connection_id": "$",
            "credential_preview": {
                "@type": "issue-credential/2.0/credential-preview",
                "attributes": [
                {"name": "data", "value": "test"}
                ]
            },
            "filter": {
                "indy": {
                "cred_def_id": "#1#",
                "issuer_did": "#2#",
                "schema_id": "#3#",
                "schema_issuer_did": "#2#",
                "schema_name": "#4#",
                "schema_version": "#5#"
                },
                "trace": false
            }
            }
        """
        body = body.replace("$",connectionid)
        body = body.replace("#1#",Server(GetServerID()).node.creddefid).replace("#2#",Server(GetServerID()).node.did).replace("#3#",Server(GetServerID()).node.schemaid).replace("#4#",Server(GetServerID()).node.schemaid.split(":")[2]).replace("#5#",Server(GetServerID()).node.schemaid.split(":")[3])
        jsl = json.loads(self.pcfdataexchange)
        #print(jsl)
        body = body.replace("%1%",jsl['version']).replace("%2%",str(jsl['created'])).replace("%3%",jsl['companyName']).replace("%4%",str(jsl['companyIds'])).replace("%5%",jsl['productDescription']).replace("%6%",str(jsl['productIds'])).replace("%7%",jsl['productCategoryCpc']).replace("%8%",jsl['productNameCompany']).replace("%9%",jsl['comment']).replace("%10%",jsl['pcf'])
        print(json.dumps(json.loads(body),indent=4))
        r=requests.post(url = self.node.endpoint_acapy2+'/issue-credential-2.0/send', json=body)
        print(json.dumps(json.loads(r.content)))

class Node:
    def __init__(self, id):
        cursor = conn_db.cursor()
        cursor.execute("SELECT * FROM Nodes WHERE NodeID = {}".format(id))
        result1 = cursor.fetchone()

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
        self.connections = {}
        self.products = []
        self.products_list = []
        
        
        if not result1[11] == "N/A":
            temp = json.loads(result1[11])
            
            for element in temp:
                self.connections[element[0]] = element[1]

        if self.type == "server":
            cursor.execute("SELECT ProductID FROM Products")
            result2 = [i[0] for i in cursor.fetchall()]
            for id in result2:
                self.products.append(Product(id))
        elif self.type == "client":
            cursor.execute("SELECT ProductID FROM Products WHERE NodeID = {}".format(id))
            result2 = [i[0] for i in cursor.fetchall()]
            for id in result2:
                self.products.append(Product(id))
        for element in self.products:
            self.products_list.append([element.id,element.name,element.description,element.pcfdataexchange,element.company,element.credential])

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
        cursor = conn_db.cursor()
        cursor.execute("SELECT Connections FROM Nodes WHERE NodeID = {}".format(self.id))
        result = cursor.fetchone()[0]

        if result == "N/A":
            data = []
            data.append([int(id),response2])
            data = json.dumps(data)
        else:
            data = ast.literal_eval(result)
            data.append([int(id),response2])
            data = json.dumps(data)
        

        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET Connections = '{}' WHERE NodeID={}".format(data,self.id)
        cursor.execute(sql)
        conn_db.commit()

        # Register into DB - Node 2
        cursor = conn_db.cursor()
        cursor.execute("SELECT Connections FROM Nodes WHERE NodeID = {}".format(id))
        result = cursor.fetchone()[0]

        if result == "N/A":
            data = []
            data.append([int(self.id),response4])
            data = json.dumps(data)
        else:
            data = ast.literal_eval(result)
            data.append([int(self.id),response4])
            data = json.dumps(data)
        

        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET Connections = '{}' WHERE NodeID={}".format(data,id)
        cursor.execute(sql)
        conn_db.commit()

    def Register(self):
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
        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET DID = '{}' WHERE NodeID = {}".format(did,self.id)
        cursor.execute(sql)
        conn_db.commit()

        # Register Schema
        #{"specVersion": "ver1", "version": "ver1", "created": 1717371325, "status": "Active", "companyName": "Siemens", "companyIds": 201, "productDescription": "descp1", "productIds": "101", "productCategoryCpc": "cpc1", "productNameCompany": "name1", "comment": "comment1", "pcf": "pcf1"}
        body = json.loads('{"attributes": ["data"],"schema_name": "PCF","schema_version": "1.0"}')
        r=requests.post(url = self.endpoint_acapy2+'/schemas', json=body)
        schema_id = json.loads(r.content)['sent']['schema_id']

        # Register into DB
        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET SchemaID = '{}' WHERE NodeID={}".format(schema_id,self.id)
        cursor.execute(sql)
        conn_db.commit()

        # Regsiter Credential Definition
        cursor = conn_db.cursor()
        cursor.execute("SELECT SchemaID FROM Nodes WHERE NodeID={}".format(self.id))
        schema_id = cursor.fetchone()[0]

        body = json.loads('{"revocation_registry_size": 1000,"schema_id": "#","support_revocation": true,"tag": "default"}'.replace("#",schema_id))
        r=requests.post(url = self.endpoint_acapy2+'/credential-definitions', json=body)
        credential_definition_id = json.loads(r.content)['sent']['credential_definition_id']

        # Register into DB
        cursor = conn_db.cursor()
        sql = "UPDATE Nodes SET CredDefID = '{}' WHERE NodeID={}".format(credential_definition_id,self.id)
        cursor.execute(sql)
        conn_db.commit()

        if self.type == "client":
            self.Connect(GetServerID())

class Client(Node):
  def __init__(self,id):
    self.node = Node(id)
    
    cursor = conn_db.cursor()
    cursor.execute("SELECT * FROM Nodes WHERE NodeID!={} AND NodeID!={}".format(self.node.id,GetServerID()))
    self.suppliers = [list(i) for i in list(cursor.fetchall())]
    self.supplychain = []
    self.connection_server = "N/A"
    self.connected_nodes = []

    if not self.node.connections == "N/A":
        for id in list(self.node.connections.keys()):
            cursor = conn_db.cursor()
            cursor.execute("SELECT * FROM Products WHERE NodeID={}".format(id))
            self.supplychain = cursor.fetchall()

        if not self.node.connections == {}:
            if self.node.type == "client":
                self.connection_server = self.node.connections[GetServerID()]
        else:
            self.connection_server = "N/A"
    
    #print(self.suppliers)
    for element in self.suppliers:
        #print(type(element[11]))
        #print([i for i in element[11]])
        if not element[11] == "N/A":
            if not self.node.id in [i[0] for i in json.loads(element[11])]:
                element.append(False)
            else:
                element.append(self.node.connections[element[0]])

  def RegisterProduct(self,productId,productName,version,productDescription,productCategoryCpc,pcf,comment):
      data = {
      "specVersion": version,
      "version": version,
      "created": round(time.time()),
      "status": "Active",
      "companyName": self.node.name,
      "companyIds": self.node.id,
      "productDescription": productDescription,
      "productIds": productId,
      "productCategoryCpc": productCategoryCpc,
      "productNameCompany": productName,
      "comment": comment,
      "pcf": pcf
      }

      # Convert dictionary to JSON format
      data = json.dumps(data)

      try:
        cursor = conn_db.cursor()
        sql = "INSERT INTO Products (ProductID, ProductName, ProductDescription, PCFDataExchange, CredentialID, NodeID) VALUES ({}, '{}', '{}', '{}', '{}', {})".format(productId,productName,productDescription,data,"N/A",self.node.id)
        cursor.execute(sql)
        conn_db.commit()
        Notification(200,"New product from #{}.",self.node.id)
      except Exception as e:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          print("Line :{}\n".format(exc_tb.tb_lineno,str(e)))

class Server(Node):
    def __init__(self, id):
        self.node = Node(id)