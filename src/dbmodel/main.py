'''
Created on 19 Mar 2018

@author: shane, sean, oz
'''
#code adapted from https://www.youtube.com/watch?v=kRNXKzfYrPU

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sos:ozflanagan1@sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com/sosdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class BikeData(db.Model):
    __tablename__ = 'bike'
    number = db.Column('number', db.Integer, primary_key = True)
    street = db.Column('street', db.Unicode)
    address = db.Column('address', db.Unicode)
    lat = db.Column('lat', db.Float)
    lng = db.Column('lng', db.Float)
    banking = db.Column('banking', db.Unicode)
    bonus = db.Column('bonus', db.Unicode)
    status = db.Column('status', db.Unicode)
    contract = db.Column('contract', db.Unicode)
    stands = db.Column('stands', db.Integer)
    a_stands = db.Column('a_stands', db.Integer)
    a_bikes = db.Column('a_bikes', db.Integer)
    timestamp = db.Column('timestamp', db.BigInteger, primary_key = True)
    
class BikeSchema(ma.ModelSchema):
    class Meta:
        model = BikeData
        