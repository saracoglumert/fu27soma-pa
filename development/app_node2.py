from flask import Flask, render_template, request, redirect
from datetime import datetime
import sys
import os
import inspect
import controller2 as controller

sys.pycache_prefix = "/root/cache"

CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

app = Flask(__name__,template_folder='view_node')

@app.route('/')
def main():
    title = controller.Client(CONFIG_NODEID).node.name
    CompanyID = CONFIG_NODEID
    ConnectionID = controller.Client(CONFIG_NODEID).connection_server
    DID = controller.Client(CONFIG_NODEID).node.did
    SchemaID = controller.Client(CONFIG_NODEID).node.schemaid
    CredDefID = controller.Client(CONFIG_NODEID).node.creddefid
    if DID == "N/A" and SchemaID == "N/A" and CredDefID == "N/A":
        registered = False
    else:
        registered = True
    notifications = []
    return render_template('home.html',title=title,CompanyID=CompanyID,ConnectionID=ConnectionID,DID=DID,SchemaID=SchemaID,CredDefID=CredDefID,registered=registered,notifications=notifications)

@app.route('/products')
def handler_products():
    products = controller.Client(CONFIG_NODEID).node.products_list
    #products = []
    return render_template('products.html',title=controller.Client(CONFIG_NODEID).node.name,products=products)

@app.route('/supplychain')
def handler_supplychain():
    products = controller.Client(CONFIG_NODEID).supplychain
    companies = controller.Client(CONFIG_NODEID).suppliers
    connections = controller.Client(CONFIG_NODEID).node.connections
    if not CONFIG_NODEID in list(connections.keys()):
        connected = False
        connected = False
    else:
        connected = True
    return render_template('supplychain.html',title=controller.Client(CONFIG_NODEID).node.name,companies=companies,products=products,connected=connected,connid=connections)

@app.route('/request', methods = ['POST'])
def handler_request():
    ProductID = request.form["ProductID"]
    #return redirect("/", code=302)
    return ('', 204)

@app.route('/connect', methods = ['POST'])
def handler_connect():
    CompanyID = request.form["CompanyID"]
    controller.Client(CONFIG_NODEID).node.Connect(CompanyID)
    return redirect("/supplychain", code=302)
    #return ('', 204)

@app.route('/register', methods = ['POST'])
def handler_register():
    CompanyID = request.form["CompanyID"]
    controller.Client(CONFIG_NODEID).node.Register()
    return redirect("/", code=302)
    #return ('', 204)

@app.route('/newproduct', methods = ['POST'])
def handler_newproduct():
    productId = request.form["productId"]
    productNameCompany = request.form["productNameCompany"]
    version = request.form["version"]
    productDescription = request.form["productDescription"]
    productCategoryCpc = request.form["productCategoryCpc"]
    pcf = request.form["pcf"]
    comment = request.form["comment"]

    controller.Client(CONFIG_NODEID).RegisterProduct(productId,productNameCompany,version,productDescription,productCategoryCpc,pcf,comment)

    print("heyo")
    return redirect("/products", code=302)
    #return ('', 204)

if __name__ == "__main__":
    #CONFIG_NODEID = int(sys.argv[1])
    #port = int(sys.argv[2])
    CONFIG_NODEID = 202
    port = 2002
    app.run(host='0.0.0.0', port=port, debug=False)