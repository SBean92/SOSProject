'''
Created on 19 Mar 2018

@author: shane, sean, oz
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sos:ozflanagan1@sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com/sosdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Bike_data(db.Model):
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
    
    def __init__(self, number, street, address, lat, lng, banking, bonus, status, contract, stands, a_stands, a_bikes, timestamp):
        self.number = number
        self.street = street
        self.address = address
        self.lat = lat
        self.lng = lng
        self.banking = banking
        self.bonus = bonus
        self.status = status
        self.contract =  contract
        self.stands = stands
        self.a_stands = a_stands
        self.a_bikes = a_bikes
        self.timestamp = timestamp

#Code adapted from http://piotr.banaszkiewicz.org/blog/2012/06/30/serialize-sqlalchemy-results-into-json/       
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'number': self.number,
           'street': self.street,
           'address': self.address,
           'lat': self.lat,
           'lng': self.lng,
           'banking': self.banking,
           'bonus': self.bonus,
           'status': self.status,
           'contract': self.contract,
           'stands': self.stands,
           'a_stands': self.a_stands,
           'a_bikes': self.a_bikes,
           'timestamp': self.timestamp
       }