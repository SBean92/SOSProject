from jsonschema.validators import requests
import json


#Read in weather info and put into JSON Dump. Currently only doing it once
#This is for the whole day, can change this to current if we need, not much difference
"""response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=4f2499afbefdfe83bed8ceeca402adc5")
weather = response.json()
with open('data.txt', 'w') as outfile:
    json.dump(weather, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)"""


#Just reading in from here so I don't get kicked off the API

with open('data.txt') as json_data:
    weather = json.load(json_data)


#Regardless of whether current/ forecast this will be same
#essentially taking in list in weather and seeing if any of rain codes present
# if they are then have 1 value for rain, if not then 0 value for not raining

weather= weather['list']
rain_codes=[200,201,202,210,211,212,
            221,230,231,232,300,301,
            302,310,311,312,313,314,
            321,500,501,502,503,504,
            511,520,521,522,531,600,
            601,602,611,612,615,616,
            620,621,622]

#Appends date, raining yes/no and overall description to list
for i in weather:
    weather_list=[]
    weather_list.append(i['dt_txt'])
    is_raining= (i['weather'][0]['id'])
    if is_raining in rain_codes:
        weather_list.append(1)
    else:
        weather_list.append(0)
    weather_list.append(i['weather'][0]['description'])
    print(weather_list)
    
#need a way to put list into DB for weather
                 
        


"""for key, value in i.items():  
    with open(r"weather.csv", 'a') as csvfile:
        weather_writer = csv.writer(csvfile, lineterminator = '\n')
        weather_writer.writerow(weather_list)"""
