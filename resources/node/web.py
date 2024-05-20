from flask import Flask, render_template, request, redirect
from datetime import datetime
import sys
import os
import inspect
import controller_db

CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

app = Flask(__name__)

notifications = []

@app.route('/')
def main():
    return render_template('index.html',title=CONFIG_COMPANYNAME,notifications=notifications)

@app.route('/products')
def handler_products():
    products = controller_db.Company(CONFIG_COMPANYID).ProductstoList()
    return render_template('products.html',title=CONFIG_COMPANYNAME,products=products)

@app.route('/supplychain')
def handler_supplychain():
    products = controller_db.SupplyChain(CONFIG_COMPANYID).ProductstoList()
    companies = controller_db.SupplyChain(CONFIG_COMPANYID).CompaniestoList()
    return render_template('supplychain.html',title=CONFIG_COMPANYNAME,companies=companies,products=products)

@app.route('/request', methods = ['POST'])
def handler_request():
    ProductID = request.form["ProductID"]

    stamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    notifications.append("<b>{}</b> - PCF data requested for #{}.".format(stamp,ProductID))
    #return redirect("/", code=302)
    return ('', 204)

@app.route('/connect', methods = ['POST'])
def handler_connect():
    CompanyID = request.form["CompanyID"]

    stamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    notifications.append("<b>{}</b> - Connection requested for #{}.".format(stamp,CompanyID))
    #return redirect("/", code=302)
    return ('', 204)

if __name__ == "__main__":
    CONFIG_COMPANYID = int(sys.argv[1])
    CONFIG_COMPANYNAME = controller_db.Company(CONFIG_COMPANYID).name
    app.run(host='0.0.0.0', port=%port_ui%, debug=False)