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

class Guys(db.Model):
    __tablename__ = 'test'
    name = db.Column('name', db.Unicode, primary_key = True)
    height = db.Column('height', db.Integer)
    width = db.Column('width', db.Integer)
    
    def __init__(self, name, height, width):
        self.name = name
        self.height = height
        self.width = width

#Code adapted from http://piotr.banaszkiewicz.org/blog/2012/06/30/serialize-sqlalchemy-results-into-json/       
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'height': self.height,
           'width': self.width
       }