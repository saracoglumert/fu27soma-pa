import mysql.connector


db = mysql.connector.connect(
  host="%network_ip%",
  user="%db_user%",
  password="%db_pass%",
  database="%db_name%")

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

class Company:
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
            self.ip = result1[2]
            self.port_ui = result1[3]
            self.port_acapy = result1[4]
            self.endpoint_ui = "http://{}:{}".format(result1[2],result1[3])
            self.endpoint_acapy = "http://{}:{}".format(result1[2],result1[4])
            self.products = result3
        except Exception as e:
            print(str(e))
    
    def ProductstoList(self):
        temp = []
        for element in self.products:
            temp.append([element.id,element.name,element.pcf,element.company])
        return temp

class SupplyChain:
    def __init__(self,id):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT NodeID FROM Nodes WHERE NodeID!={} AND NodeID!={}".format(id,GetServerID()))
            result1 = [i[0] for i in cursor.fetchall()]
            result2 = []
            for id in result1:
                result2.append(Company(id))

            self.companies = result2
        except Exception as e:
            print(str(e))

    def CompaniestoList(self):
        temp = []
        for element in self.companies:
            temp.append([element.id,element.name,element.ip,element.port_ui,element.port_acapy,element.endpoint_ui,element.endpoint_acapy,element.products,len(element.products)])
        return temp
    
    def ProductstoList(self):
        temp1 = []
        temp2 = []
        for productsofcompany in self.companies:
            temp1.append(productsofcompany.products)
        for productsofcompany in temp1:
            for product in productsofcompany:
                temp2.append([product.id,product.name,product.pcf,product.company,Company(product.company).name])
        return temp2

def Endpoints():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Nodes")
    results = cursor.fetchall()
    
    temp = []

    for result in results:
        temp.append([result[0],result[1],result[2],result[3],"http://{}:{}".format(result[3],result[4]),"http://{}:{}".format(result[3],result[5])])

    return temp

def GetServerID():
    cursor = db.cursor()
    cursor.execute("SELECT NodeID FROM Nodes WHERE NodeType='server'")
    result = cursor.fetchone()[0]
    
    return result