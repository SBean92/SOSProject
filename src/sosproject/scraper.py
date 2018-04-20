'''
Created on 16 Mar 2018

@author: shane, sean, oz

Practice for learning to access API
'''
from jsonschema.validators import requests
import csv
import time
import os
import MySQLdb
import traceback
from collections import OrderedDict

# Gets data from JCDecaux, writes to csv
def scraper():
    try:
        os.remove('bikes.csv')
        os.remove('static.csv')
    except OSError:
        pass
    
    response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=cf7b17e2c126f2e1998430272919516c5acb5538")
    data = response.json(object_pairs_hook=OrderedDict)

    for i in data:
        myliststatic=[]
        mylistdynamic=[]
        for key, value in i.items():
            if key == "number":
                myliststatic.append(value)
                mylistdynamic.append(value)
            elif key == "position":
                for new_key, new_value in value.items():
                    myliststatic.append(new_value)
            elif key == "name" or key == "address" or key == "contract_name":
                myliststatic.append(value)
            else:
                mylistdynamic.append(value)
        
        with open(r"bikes.csv", 'a') as csvfile:
                bike_writer = csv.writer(csvfile, lineterminator = '\n')
                bike_writer.writerow(mylistdynamic)

        with open(r"static.csv", 'a') as csvfile:
                static_writer = csv.writer(csvfile, lineterminator = '\n')
                static_writer.writerow(myliststatic)

def stationCount():
    count = 0
    csv_data = csv.reader(open('bikes.csv', 'r'))
    for row in csv_data:
        count += 1
    return count

# Creates table on AWS database
def createTable(table):
    conn = MySQLdb.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    cursor = conn.cursor()    
    if table == 'bike':
        cursor.execute('CREATE TABLE bike (number int(20) NOT NULL,street varchar(50),address varchar(50),lat float,lng float,banking varchar(5),bonus varchar(5),status varchar(10),contract varchar(10),stands int(3),a_stands int(3),a_bikes int(3),timestamp bigint(20) NOT NULL,CONSTRAINT PK_bike PRIMARY KEY (number,timestamp))')
        conn.commit()
    elif table == 'static':
        cursor.execute('CREATE TABLE bike_static(number int(4) NOT NULL, contract varchar(10), street varchar(50), address varchar(50), lat float, lng float, PRIMARY KEY (number),FOREIGN KEY (number) REFERENCES bike(number))')
        conn.commit()
    cursor.close()

def tableExist(table):
    conn = MySQLdb.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE'"+table+"'")
    if cursor.fetchone():
        cursor.close()
        return True
    else:
        cursor.close()
        return False

# Writes to table on AWS database
def sqlWrite(table):
    conn = MySQLdb.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    cursor = conn.cursor()
    if table == 'bike':
        lines = 0
        csv_data = csv.reader(open('bikes.csv', 'r'))
        for row in csv_data:
            lines += 1
            cursor.execute('INSERT INTO bike(number, banking, bonus, status, stands, a_stands, a_bikes, timestamp)' +
                            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', row)
        conn.commit()
        print("Inserting",lines,"lines into dynamic table")
    if table == 'static':
        lines = 0
        csv_data = csv.reader(open('static.csv', 'r'))
        for row in csv_data:
            lines += 1
            cursor.execute('INSERT INTO bike_static(number, street, address, lat, lng, contract)' +
                            'VALUES(%s, %s, %s, %s, %s, %s)', row)
        conn.commit()
        print("Inserting",lines,"lines into static table")     
    cursor.close()    

def main():
    oldMaxStations = 0
    while True:
        if tableExist("bike"):
            pass
        else:
            createTable("bike")
        if tableExist("bike_static"):
            pass
        else:
            createTable("static")
        try:
            scraper()
        except Exception:
            print("Error in getting data")
            traceback.print_exc()
        try:
            sqlWrite("bike")
        except Exception:
            print("Error in inserting data into bike")
            traceback.print_exc()
        newMaxStations = stationCount()
        if oldMaxStations != newMaxStations:
            try:
                sqlWrite("static")
            except Exception:
                print("Error in inserting data into static")
                traceback.print_exc()
            oldMaxStations = newMaxStations
        time.sleep(600)

if __name__ == "__main__":
    main()