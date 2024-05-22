from flask import Flask, render_template, request, redirect
from datetime import datetime
import sys
import os
import inspect
import controller


CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

app = Flask(__name__)

notifications = []

@app.route('/')
def main():
    title = CONFIG_COMPANYNAME
    CompanyID = CONFIG_COMPANYID
    DID = controller.Node(CONFIG_COMPANYID).did
    SchemaID = controller.Node(CONFIG_COMPANYID).schemaid
    CredDefID = controller.Node(CONFIG_COMPANYID).creddefid
    if DID == "N/A" and SchemaID == "N/A" and CredDefID == "N/A":
        registered = False
    else:
        registered = True
    notifications = []
    return render_template('index.html',title=title,CompanyID=CompanyID,DID=DID,SchemaID=SchemaID,CredDefID=CredDefID,registered=registered,notifications=notifications)

@app.route('/products')
def handler_products():
    products = controller.Node(CONFIG_COMPANYID).ProductstoList()
    return render_template('products.html',title=CONFIG_COMPANYNAME,products=products)

@app.route('/supplychain')
def handler_supplychain():
    products = controller.SupplyChain(CONFIG_COMPANYID).ProductstoList()
    companies = controller.SupplyChain(CONFIG_COMPANYID).CompaniestoList()
    connid = controller.Node(CONFIG_COMPANYID).connectionid
    if connid == "N/A":
        connected = False
    else:
        connected = True
    return render_template('supplychain.html',title=CONFIG_COMPANYNAME,companies=companies,products=products,connected=connected,connid=connid)

@app.route('/request', methods = ['POST'])
def handler_request():
    ProductID = request.form["ProductID"]
    stamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    notifications.insert(0,"<b>{}</b> - Requested proof for product #{}.".format(stamp,ProductID))
    #return redirect("/", code=302)
    return ('', 204)

@app.route('/connect', methods = ['POST'])
def handler_connect():
    CompanyID = request.form["CompanyID"]
    controller.Node(CONFIG_COMPANYID).Connect(CompanyID)
    return redirect("/supplychain", code=302)
    #return ('', 204)

@app.route('/issue', methods = ['POST'])
def handler_issue():
    CompanyID = request.form["ProductID"]
    stamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    notifications.insert(0,"<b>{}</b> - Issue credential for product #{}.".format(stamp,CompanyID))
    #return redirect("/", code=302)
    return ('', 204)

@app.route('/register', methods = ['POST'])
def handler_register():
    CompanyID = request.form["CompanyID"]
    controller.Node(CompanyID).RegisterDID()
    controller.Node(CompanyID).RegisterSchema()
    controller.Node(CompanyID).RegisterCredentialDefinition()
    return redirect("/", code=302)
    #return ('', 204)

if __name__ == "__main__":
    CONFIG_COMPANYID = int(sys.argv[1])
    port = int(sys.argv[2])
    CONFIG_COMPANYNAME = controller.Node(CONFIG_COMPANYID).name
    app.run(host='0.0.0.0', port=port, debug=False)