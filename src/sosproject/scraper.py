'''
Created on 16 Mar 2018

@author: shane, sean, oz

Practice for learning to access API
'''
from jsonschema.validators import requests
import csv
import time
import os
import urllib.request as urlreq

def main():
    while True:
        try:
            os.remove('bikes.csv')
        except OSError:
            pass
        response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=cf7b17e2c126f2e1998430272919516c5acb5538")
        data = response.json()
        print(response.status_code)

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

        time.sleep(120)


if __name__ == "__main__":
    main()

    
