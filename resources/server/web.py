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
    endpoints = controller_db.Endpoints()
    return render_template('index.html',title=controller_db.Company(controller_db.GetServerID()).name,endpoints=endpoints)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=%port_ui%, debug=False)