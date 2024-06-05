from flask import Flask, render_template, request, redirect
from datetime import datetime
import sys
import os
import inspect
import controller2 as controller

sys.pycache_prefix = "/root/cache"

CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

app = Flask(__name__,template_folder='view_server')

@app.route('/')
def main():
    title = controller.Server(CONFIG_NODEID).node.name
    CompanyID = CONFIG_NODEID
    DID = controller.Server(CONFIG_NODEID).node.did
    SchemaID = controller.Server(CONFIG_NODEID).node.schemaid
    CredDefID = controller.Server(CONFIG_NODEID).node.creddefid
    if DID == "N/A" and SchemaID == "N/A" and CredDefID == "N/A":
        registered = False
    else:
        registered = True
    notifications = []
    return render_template('home.html',title=title,CompanyID=CompanyID,DID=DID,SchemaID=SchemaID,CredDefID=CredDefID,registered=registered,notifications=notifications)

@app.route('/products')
def handler_products():
    products = controller.Server(CONFIG_NODEID).node.products_list
    return render_template('products.html',title=controller.Client(CONFIG_NODEID).node.name,products=products)

@app.route('/register', methods = ['POST'])
def handler_register():
    CompanyID = request.form["CompanyID"]
    controller.Server(CONFIG_NODEID).node.Register()
    return redirect("/", code=302)
    #return ('', 204)

@app.route('/issue', methods = ['POST'])
def handler_issue():
    ProductID = request.form["ProductID"]
    print("Issue :{}".format(ProductID))
    return redirect("/products", code=302)
    #return ('', 204)

if __name__ == "__main__":
    #CONFIG_NODEID = int(sys.argv[1])
    #port = int(sys.argv[2])
    CONFIG_NODEID = 200
    port = 2000
    app.run(host='0.0.0.0', port=port, debug=False)