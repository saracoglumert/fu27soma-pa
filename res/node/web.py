from flask import Flask, render_template, request, redirect
from datetime import datetime
import mysql.connector
import sys
import os
import inspect

mydb = mysql.connector.connect(
  host="%network_ip%",
  user="%db_user%",
  password="%db_pass%",
  database="%db_name%")

CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

app = Flask(__name__)

notifications = []

@app.route('/')
def main():
    return render_template('index.html',title=CONFIG_COMPANYNAME,notifications=notifications)

@app.route('/products')
def handler_products():
    products = getProductbyCompanyID(CONFIG_COMPANYID)
    return render_template('products.html',title=CONFIG_COMPANYNAME,products=products)

@app.route('/supplychain')
def handler_supplychain():
    products = getProductsonSupplyChainbyCompanyID(CONFIG_COMPANYID)
    return render_template('supplychain.html',title=CONFIG_COMPANYNAME,products=products)

@app.route('/request', methods = ['POST'])
def handler_request():
    productID = request.form["productID"]

    stamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    notifications.append("<b>{}</b> - PCF data requested for #{}.".format(stamp,productID))
    #return redirect("/", code=302)
    return ('', 204)

def getCompanyNamebyID(id):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Companies")
        myresult = dict(mycursor.fetchall())
        return myresult[id]
    except Exception as e:
        return "N/A - Error:"

def getProductbyID(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Products WHERE ProductID={}".format(id))
    myresult = mycursor.fetchone()
    return myresult

def getProductbyCompanyID(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Products WHERE CompanyID={}".format(id))
    myresult = list(mycursor.fetchall())
    return myresult

def getProductsonSupplyChainbyCompanyID(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT productID, productName, companyID FROM Products WHERE companyID!={}".format(id))
    myresult = list(mycursor.fetchall())
    result = []
    for element in myresult:
        temp = (element[0],element[2],getCompanyNamebyID(element[2]),element[1])
        result.append(temp)
    return result

if __name__ == "__main__":
    CONFIG_COMPANYID = int(sys.argv[1])
    CONFIG_COMPANYNAME = getCompanyNamebyID(CONFIG_COMPANYID)
    app.run(host='0.0.0.0', port=80, debug=False)