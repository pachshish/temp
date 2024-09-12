import math
import json
from datetime import datetime, timedelta

import requests

from apirequests import wather
from models.pilotModel import pilot
from models.aircraftModel import aircraft
from models.targetModel import target

pilot_data = {}
file_path = "jsonFile/pilots.json"
with open(file_path, "r") as file:
       list_of_pilot = json.load(file)
print(list_of_pilot)


def make_pilot_model(pilot_data):
    pilots = []
    for name, details in pilot_data:
        pilots.append(pilot(name, details[0]))
    return pilots
print(make_pilot_model(list_of_pilot))

target_data = {}
file_path = "jsonFile/targets.json"
with open(file_path, "r") as file:
       data_target = json.load(file)
print(data_target)

# def make_target_model(data_target):
#     targets = []
#     for name, details, e in data_target:
#         targets.append(target(name, details[0], e[1]))
#     return targets
# print(make_target_model(data_target))

aircraft_data = {}
aircraft_path = "jsonFile/aircrafts.json"
with open(aircraft_path, "r") as file:
    data_aircraft = json.load(file)
print(data_aircraft)

# def make_aircraft_model(data_aircraft):
#     aircrafts = []
#     for name, details in data_aircraft:
#         aircrafts.append(aircraft(name, details[0], details[1]))
#     return aircrafts
# print(make_aircraft_model(data_aircraft))

def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371.0 # Radius of the Earth in kilometers
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Calculate differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Calculate the distance
    distance = r * c
    return distance

def get_distans():
    key = '058d0d991059cd8065248e59b1b4c8bb'
    distanses = []
    jerusalem_lat = 31.76944
    jerusalem_lon = 35.21306
    for i in range(len(data_target)):
        city = data_target[i]['City']
        distans_city = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={key}'
        response = requests.get(distans_city)
        lat = response.json()[0]['lat']
        lon = response.json()[0]['lon']
        distans = str(haversine_distance(jerusalem_lat, jerusalem_lon, lat, lon))
        distanses.append((city, distans))
        print(f'The distance from {city} to israel is {distans} kilometers.')
    # for j in range(len(distanses)):
    #     print(f'The distance to {distanses[j][0]} is {distanses[j][1]} kilometers.')
    return distanses

print(get_distans())

def weather_score(weather):
    cloud = weather["clouds"]
    if cloud != "0":
        cloud = cloud / 100
    speed = weather["wind_speed"]
    if speed != "0":
        speed = speed / 10
    if weather["weather"] == "Clear":
        return (1 + speed + cloud) / 3 * 100
    elif weather["weather"] == "Clouds":
        return (0.7 + speed + cloud) / 3 * 100
    elif weather["weather"] == "Rain":
        return (0.4 + speed + cloud) / 3 * 100
    elif weather["weather"] == "Stormy":
        return (0.2 + speed + cloud) / 3 * 100
    else:
        return (0 + speed + cloud) / 3 * 100



def get_weather():
    key = '058d0d991059cd8065248e59b1b4c8bb'
    weathers = []
    for i in range(len(data_target)):
        city = data_target[i]['City']
        weather_city = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}'
        response = requests.get(weather_city).json()
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)  # חצות הקרוב
        forecasts = response["list"]
        selected_forecasts = []
        for forecast in forecasts:
            forecast_time = datetime.strptime(forecast['dt_txt'], "%Y-%m-%d %H:%M:%S")
            if forecast_time.hour == 0 and forecast_time >= midnight:
                selected_forecasts = ({
                    'weather': forecast['weather'][0]['main'],
                    'clouds': forecast['clouds']['all'],
                    'wind_speed': forecast['wind']['speed']
                })
        weather_city = weather_score(selected_forecasts)
        weathers.append((city, weather_city))
        print(f'The weather in {city} is {weather_city} ideal percent.')
    return weathers

print(get_weather())


def calculate_mission():
    list_of_pilot
    for i in list_of_pilot:
        print (list_of_pilot[i]['skill_level'])


calculate_mission()
