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
            f = urlreq.urlopen('https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1pVPKJxD6Bdmfv6dO-eHXw-YsJSO5QBDyIoiGuxh3n9k%2Fedit%3Fusp%3Dsharing&h=ATOVrf9M0f9t3wjassGzf9wEVHyBZRb_qXA0_xwilGMWH7qk8CzTg_ixgsMj9ucpZn9tHhrQhlwdGILJKBX7asMAjkzGHMOKqBvU5A-ALmtRkLB4-Ply2w')

            with open(f, 'a') as csvfile:
                bike_writer = csv.writer(csvfile, lineterminator = '\n')
                bike_writer.writerow(mylist)
                r = requests.post('https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1pVPKJxD6Bdmfv6dO-eHXw-YsJSO5QBDyIoiGuxh3n9k%2Fedit%3Fusp%3Dsharing&h=ATOVrf9M0f9t3wjassGzf9wEVHyBZRb_qXA0_xwilGMWH7qk8CzTg_ixgsMj9ucpZn9tHhrQhlwdGILJKBX7asMAjkzGHMOKqBvU5A-ALmtRkLB4-Ply2w', files={'bikes.csv': f})

        time.sleep(120)


if __name__ == "__main__":
    main()

    
