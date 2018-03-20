'''
Created on 20 Mar 2018

@author: shane, sean, oz
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbmodel.main import Guys
import pymysql
pymysql.install_as_MySQLdb()
from flask.json import jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sos:ozflanagan1@sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com/sosdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')

def display():
   guys = Guys.query.all()
   return jsonify([i.serialize for i in guys])

if __name__ == "__main__":
    app.run(debug=True)
