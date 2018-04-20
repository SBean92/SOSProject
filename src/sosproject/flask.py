'''
Created on 20 Mar 2018

@author: shane, sean, oz
'''
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dbmodel.main import StaticBikeData, DynamicBikeData, StaticBikeSchema, DynamicBikeSchema, AvgBikeData, AvgBikeSchema, DailyWeatherData, DailyWeatherSchema, HourlyWeatherData, HourlyWeatherSchema,\
    AvgBikeDataDay, AvgBikeDaySchema
import pymysql
pymysql.install_as_MySQLdb()
from flask.json import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sos:ozflanagan1@sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com/sosdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/root1')
# Root 1 contains station location and id data
def display1():
    static_bike_data = StaticBikeData.query.all()
    static_bike_schema = StaticBikeSchema(many=True)
    static_output = static_bike_schema.dump(static_bike_data).data
    return jsonify(static_output)

@app.route('/root2')
# Root 2 contains station available bike and stands data
def display2():
    dynamic_bike_data = DynamicBikeData.query.all()
    dynamic_bike_schema = DynamicBikeSchema(many=True)
    dynamic_output = dynamic_bike_schema.dump(dynamic_bike_data).data
    return jsonify(dynamic_output)

@app.route('/root3')
# Root 3 contains most recent station available bike and stands data
def display3():
    live_bike_data = db.engine.execute('SELECT number, LatestUpdate, banking, bonus, status, stands, a_stands, a_bikes FROM(SELECT * FROM bike INNER JOIN (SELECT MAX(timestamp) AS LatestUpdate, number AS number2 FROM bike GROUP BY number2) SubMax ON bike.timestamp = SubMax.LatestUpdate and bike.number = SubMax.number2)bikeLatest;')
    live_bike_schema = DynamicBikeSchema(many=True)
    live_output = live_bike_schema.dump(live_bike_data).data
    return jsonify(root3=live_output)

@app.route('/root4')
# Root 4 contains average bike and stands data by hour 
def display4():
    avg_bike_data = AvgBikeData.query.all()
    avg_bike_schema = AvgBikeSchema(many=True)
    avg_output = avg_bike_schema.dump(avg_bike_data).data
    return jsonify(root4=avg_output)

@app.route('/root5')
# Root 5 contains daily weather data
def display5():
    daily_weather_data = DailyWeatherData.query.all()
    daily_weather_schema = DailyWeatherSchema(many=True)
    daily_weather_output = daily_weather_schema.dump(daily_weather_data).data
    return jsonify(root5=daily_weather_output)

@app.route('/root6')
# Root 5 contains hourly weather data
def display6():
    hourly_weather_data = HourlyWeatherData.query.all()
    hourly_weather_schema = HourlyWeatherSchema(many=True)
    hourly_weather_output = hourly_weather_schema.dump(hourly_weather_data).data
    return jsonify(root6=hourly_weather_output)

@app.route('/root7')
# Root 7 contains average bike and stands data by day
def display7():
    avg_bike_data_day = AvgBikeDataDay.query.all()
    avg_bike_schema_day = AvgBikeDaySchema(many=True)
    avg_day_output = avg_bike_schema_day.dump(avg_bike_data_day).data
    return jsonify(root7=avg_day_output)

if __name__ == "__main__":
    app.run(debug=True)
    
