from flask import Flask, render_template, request, redirect
from datetime import datetime
import sys
import os
import inspect
import controller

sys.pycache_prefix = "/root/cache"

CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

app = Flask(__name__,template_folder='/root/view')

@app.route('/')
def main():
    node.update()
    return render_template('home.html',node=node)

@app.route('/products')
def handler_products():
    
    node.update()
    return render_template('products.html',node=node,controller=controller)

@app.route('/register', methods = ['POST'])
def handler_register():
    node.register()
    
    node.update()
    return redirect("/", code=302)

@app.route('/issue', methods = ['POST'])
def handler_issue():
    node.IssueCredential(request.form["ProductID"])
    
    node.update()
    return redirect("/products", code=302)

if __name__ == "__main__":
    CONFIG_NODEID = int(sys.argv[1])
    port = int(sys.argv[2])
    node = controller.Server(CONFIG_NODEID)
    app.run(host='0.0.0.0', port=port, debug=False)