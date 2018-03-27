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
#from collections import OrderedDict

def scraper():
    try:
        os.remove('bikes.csv')
    except OSError:
        pass
    #d = OrderedDict()
    #d['number'] = 1
    #d['name'] = 2
    #d['address'] = 3
    #d['position'] = 4
    #d['banking'] = 5
    #d['bonus'] = 6
    #d['status'] = 7
    #d['contract_name'] = 8
    #d['bike_stands'] = 9
    #d['available_bike_stands'] = 10
    #d['available_bikes'] = 11
    #d['last_update'] = 12
    response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=cf7b17e2c126f2e1998430272919516c5acb5538")
    data = response.json()

    for i in data:
        mylist=[]
        for key, value in i.items():
            if key == "position":
                for new_key, new_value in value.items():
                    mylist.append(new_value)
            else:
                mylist.append(value)
        

        with open(r"bikes.csv", 'a') as csvfile:
            bike_writer = csv.writer(csvfile, lineterminator = '\n')
            bike_writer.writerow(mylist)

def sqlWrite():
    lines = 0
    conn = MySQLdb.connect(host = 'sos-database.cvwfzmigbgkv.us-west-2.rds.amazonaws.com', user = 'sos', passwd = 'ozflanagan1', db = 'sosdatabase')
    cursor = conn.cursor()
    csv_data = csv.reader(open('bikes.csv', 'r'))
    for row in csv_data:
        lines += 1
        cursor.execute('INSERT INTO bike(number, street, address, lat, lng, banking, bonus, status, contract, stands, a_stands, a_bikes, timestamp)' +
                         'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', row)
    conn.commit()
    cursor.close()
    print("Inserting",lines,"lines into table")

def main():
    while True:
        try:
            scraper()
        except Exception:
            print("Error in getting data")
            traceback.print_exc()
            
        try:
            sqlWrite()
        except Exception:
            print("Error in inserting data")
            traceback.print_exc()
        time.sleep(300)

if __name__ == "__main__":
    main()