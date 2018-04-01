'''
Created on 20 Mar 2018

@author: shane, sean, oz
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbmodel.main import StaticBikeData, DynamicBikeData, StaticBikeSchema, DynamicBikeSchema
import pymysql
pymysql.install_as_MySQLdb()
from flask.json import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sos:ozflanagan1@sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com/sosdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')

def display():
    static_bike_data = StaticBikeData.query.all()
    dynamic_bike_data = DynamicBikeData.query.all()
    static_bike_schema = StaticBikeSchema(many=True)
    dynamic_bike_schema = DynamicBikeSchema(many=True)
    static_output = static_bike_schema.dump(static_bike_data).data
    dynamic_output = dynamic_bike_schema.dump(dynamic_bike_data).data
    return jsonify(static_output[0])

if __name__ == "__main__":
    app.run(debug=True)
    
