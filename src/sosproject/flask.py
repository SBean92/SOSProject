'''
Created on 20 Mar 2018

@author: shane, sean, oz
'''
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dbmodel.main import StaticBikeData, DynamicBikeData, StaticBikeSchema, DynamicBikeSchema
import pymysql
pymysql.install_as_MySQLdb()
from flask.json import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sos:ozflanagan1@sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com/sosdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/root1')

def display1():
    static_bike_data = StaticBikeData.query.all()
    static_bike_schema = StaticBikeSchema(many=True)
    static_output = static_bike_schema.dump(static_bike_data).data
    return jsonify(static_output)

@app.route('/root2')

def display2():
    dynamic_bike_data = DynamicBikeData.query.all()
    dynamic_bike_schema = DynamicBikeSchema(many=True)
    dynamic_output = dynamic_bike_schema.dump(dynamic_bike_data).data
    return jsonify(dynamic_output)

@app.route('/root3')

def display3():
    live_bike_data = db.engine.execute('SELECT number, LatestUpdate, banking, b$
    live_bike_schema = DynamicBikeSchema(many=True)
    live_output = live_bike_schema.dump(live_bike_data).data
    return jsonify(root3=live_output)

if __name__ == "__main__":
    app.run(debug=True)
    
