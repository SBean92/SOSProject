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

class StaticBikeData(db.Model):
    __tablename__ = 'bike_static'
    number = db.Column('number', db.Integer, primary_key = True)
    contract = db.Column('contract', db.Unicode)
    street = db.Column('street', db.Unicode)
    address = db.Column('address', db.Unicode)
    lat = db.Column('lat', db.Float)
    lng = db.Column('lng', db.Float)
    
class DynamicBikeData(db.Model):
    __tablename__ = 'bike'
    number = db.Column('number', db.Integer, primary_key = True)
    banking = db.Column('banking', db.Unicode)
    bonus = db.Column('bonus', db.Unicode)
    status = db.Column('status', db.Unicode)
    stands = db.Column('stands', db.Integer)
    a_stands = db.Column('a_stands', db.Integer)
    a_bikes = db.Column('a_bikes', db.Integer)
    timestamp = db.Column('timestamp', db.BigInteger, primary_key = True)
    
class AvgBikeData(db.Model):
    __tablename__ = 'averages'
    index = db.Column('index', db.Integer, primary_key = True)
    number = db.Column('number', db.Integer)
    weekday = db.Column('weekday', db.Unicode)
    hour = db.Column('hour', db.Integer)
    a_bikes = db.Column('a_stands', db.Integer)
    a_stands = db.Column('a_bikes', db.Integer)

class DailyWeatherData(db.Model):
    __tablename__ = 'daily_weather'
    timestamp = db.Column('timestamp', db.Unicode, primary_key = True)
    isRaining = db.Column('isRaining', db.Integer)
    description = db.Column('description', db.Unicode)

class HourlyWeatherData(db.Model):
    __tablename__ = 'hourly_weather'
    timestamp = db.Column('timestamp', db.Unicode, primary_key = True)
    isRaining = db.Column('isRaining', db.Integer)
    description = db.Column('description', db.Unicode)
    
class AvgBikeDataDay(db.Model):
    __tablename__ = 'averages_daily'
    index = db.Column('index', db.Integer, primary_key = True)
    number = db.Column('number', db.Integer)
    weekday = db.Column('weekday', db.Unicode)
    a_bikes = db.Column('a_stands', db.Integer)
    a_stands = db.Column('a_bikes', db.Integer)

class StaticBikeSchema(ma.ModelSchema):
    class Meta:
        model = StaticBikeData
        
class DynamicBikeSchema(ma.ModelSchema):
    class Meta:
        model = DynamicBikeData
        
class AvgBikeSchema(ma.ModelSchema):
    class Meta:
        model = AvgBikeData

class DailyWeatherSchema(ma.ModelSchema):
    class Meta:
        model = DailyWeatherData

class HourlyWeatherSchema(ma.ModelSchema):
    class Meta:
        model = HourlyWeatherData
        
class AvgBikeDaySchema(ma.ModelSchema):
    class Meta:
        model = AvgBikeDataDay
        