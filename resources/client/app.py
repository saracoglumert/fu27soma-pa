from flask import Flask, render_template, request, redirect
from datetime import datetime
import sys
import os
import inspect
import json
import controller

sys.pycache_prefix = "/root/cache"

CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

app = Flask(__name__,template_folder='/root/view')

@app.route('/')
def main():
    node.update()
    return render_template('home.html',node=node,controller=controller,json=json)

@app.route('/products')
def handler_products():
    node.update()
    return render_template('products.html',node=node)

@app.route('/supplychain')
def handler_supplychain():
    node.update()
    return render_template('supplychain.html',node=node,controller=controller,list=list)

@app.route('/request_jwt', methods = ['POST'])
def handler_request_jwt():
    result = node.requestProofJWT(request.form["id"],request.form["data"])
    print(result)
    node.update()
    if result:
        return redirect("http://www.example.com", code=302)
    else:
        return redirect("/supplychain", code=302)

@app.route('/request_acapy', methods = ['POST'])
def handler_request_acapy():
    ProductID = request.form["ProductID"]
    #return redirect("/", code=302)
    return ('', 204)

@app.route('/connect', methods = ['POST'])
def handler_connect():
    CompanyID = request.form["CompanyID"]
    node.connect(CompanyID)
    
    node.update()
    return redirect("/supplychain", code=302)


@app.route('/register', methods = ['POST'])
def handler_register():
    node.register()
    
    node.update()
    return redirect("/", code=302)

@app.route('/newproduct', methods = ['POST'])
def handler_newproduct():
    name = request.form["productName"]
    description = request.form["productDescription"]
    version = request.form["version"]
    data = request.form["data"]

    node.newProduct(name,description,version,data)
    
    node.update()
    return redirect("/products", code=302)
    #return ('', 204)

if __name__ == "__main__":
    CONFIG_NODEID = int(sys.argv[1])
    port = int(sys.argv[2])
    node = controller.Client(CONFIG_NODEID)
    app.run(host='0.0.0.0', port=port, debug=False)