import requests
import json
import pymysql
import csv
import time
import os
import traceback

def daily_scraper():
    try:
        os.remove('daily_weather.csv')
    except:
        pass
    #Read in weather info and put into JSON Dump. Currently only doing it once
    #This is for the whole day and is a forecast. Will only keep current day then overwrite on next access
    try: 
        response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=4f2499afbefdfe83bed8ceeca402adc5")
        weather_forecast = response.json()
    except:
        print("Error connecting to API")
    """with open('weather_data.txt', 'w') as outfile:
        json.dump(weather, outfile, sort_keys = True, indent = 4,
                   ensure_ascii = False)
    
    
    #Just reading in from here so I don't get kicked off the API
    #this can be deleted as soon as it all works
    with open('weather_data.txt') as json_data:
        weather_forecast = json.load(json_data)"""
    
    
    #Regardless of whether current/ forecast this will be same
    #essentially taking in list in weather and seeing if any of rain codes present
    # if they are then have 1 value for rain, if not then 0 value for not raining
    
    weather_forecast= weather_forecast['list']
    rain_codes=[200,201,202,210,211,212,
                221,230,231,232,300,301,
                302,310,311,312,313,314,
                321,500,501,502,503,504,
                511,520,521,522,531,600,
                601,602,611,612,615,616,
                620,621,622]
    
    #Appends date, raining yes/no and overall description to list
    for i in weather_forecast:
        weather_list=[]
        weather_list.append(i['dt'])
        is_raining= (i['weather'][0]['id'])
        if is_raining in rain_codes:
            weather_list.append(1)
        else:
            weather_list.append(0)
        weather_list.append(i['weather'][0]['description'])
        print("daily",weather_list)
        
    #need a way to put list into DB for weather
         
        with open(r"daily_weather.csv", 'a') as csvfile:
            weather_writer = csv.writer(csvfile, lineterminator = '\n')
            weather_writer.writerow(weather_list)
            
def hourly_weather_scraper():
    try:
        os.remove('hourly_weather.csv')
    except OSError:
        pass
    #Read in weather info and put into JSON Dump. Currently only doing it once
    #This is current data, this will be constantly stored in the db
    try:
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?id=2964574&APPID=4f2499afbefdfe83bed8ceeca402adc5")
        weather = response.json()
    except:
        print("Error connecting to API")
        
    """with open('data.txt', 'w') as outfile:
        json.dump(weather, outfile, sort_keys = True, indent = 4,
                   ensure_ascii = False)
    
    #Just reading in from here so I don't get kicked off the API
    with open('data.txt') as json_data:
        weather = json.load(json_data)"""
    
    
    #Regardless of whether current/ forecast this will be same
    #essentially taking in list in weather and seeing if any of rain codes present
    # if they are then have 1 value for rain, if not then 0 value for not raining
    rain_codes=[200,201,202,210,211,212,
                221,230,231,232,300,301,
                302,310,311,312,313,314,
                321,500,501,502,503,504,
                511,520,521,522,531,600,
                601,602,611,612,615,616,
                620,621,622]
    #Appends date, raining yes/no and overall description to list
    weather_list=[]
    weather_list.append(weather['dt'])
    if weather['weather'][0]['id'] in rain_codes:
        weather_list.append(1)
    else:
        weather_list.append(0)
    weather_list.append(weather['weather'][0]['description'])
    print("hourly",weather_list)
    with open(r"hourly_weather.csv", 'a') as csvfile:
        weather_writer = csv.writer(csvfile, lineterminator = '\n')
        weather_writer.writerow(weather_list)

def createWeatherTable(table):
    conn = pymysql.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    cursor = conn.cursor()    
    if table == 'hourly':
        cursor.execute('CREATE TABLE hourly_weather (timestamp varchar(50) NOT NULL,isRaining int(1),description varchar(150),CONSTRAINT PK_hourly PRIMARY KEY (timestamp))')
        conn.commit()
    elif table == 'daily':
        cursor.execute('CREATE TABLE daily_weather(timestamp varchar(50) NOT NULL,isRaining int(1),description varchar(150),CONSTRAINT PK_daily PRIMARY KEY (timestamp))')
        conn.commit()
    cursor.close()

def sqlWriteWeather(table):
    try:
        conn = pymysql.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    except:
        print("Problem connecting to the database")
    cursor = conn.cursor()
    if table == 'hourly':
        lines = 0
        csv_data = csv.reader(open('hourly_weather.csv', 'r'))
        for row in csv_data:
            lines += 1
            cursor.execute('INSERT INTO hourly_weather(timestamp, isRaining, description)' +
                            'VALUES(%s, %s, %s)', row)
        conn.commit()
        print("Inserting",lines,"lines into hourly weather table")
        
    if table == 'daily':
        lines = 0
        csv_data = csv.reader(open('daily_weather.csv', 'r'))
        for row in csv_data:
            lines += 1
            cursor.execute('INSERT INTO daily_weather(timestamp, isRaining, description)' +
                            'VALUES(%s, %s, %s)', row)
        conn.commit()
        print("Inserting",lines,"lines into daily weather table")     
    cursor.close()

def tableExist(table):
    conn = pymysql.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE'"+table+"'")
    if cursor.fetchone():
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def dropTable():
    conn = pymysql.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE daily_weather")
    cursor.close()

def main():
    while True:
        if tableExist("daily_weather"):
            dropTable()
        try:
            daily_scraper()
        except Exception:
            print("Error in getting daily data")
        createWeatherTable("daily")
        try:
            sqlWriteWeather("daily")
        except Exception:
            print("Error in inserting daily data")

        if tableExist("hourly_weather"):
            pass
        else:
            createWeatherTable("hourly")
        for x in range(0,47):
            try:
                hourly_weather_scraper()
            except Exception:
                print("Error in getting hourly data")
            try:
                sqlWriteWeather("hourly")
            except Exception:
                print("Error in inserting hourly data")
            time.sleep(1800)

if __name__ == "__main__":
    main()