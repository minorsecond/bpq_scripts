#!/bin/python
# Get wx for zip code

import requests
import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "credentials.txt")

api_key = "NULL"
config = configparser.ConfigParser()
try:
    config.read(config_path)
    api_key = config['DEFAULT']['api_key']
except KeyError:
    print("You must first create a credentials file named credentials.txt that adheres to the following format:\n")
    print("[DEFAULT]\napi_key=YOURAPIKEYHERE")

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

call = input()  # capture BPQ call sign that is sent
zip_code = None
tries = 0
if api_key != "NULL":
    while zip_code is None or len(zip_code) != 5 and type(zip_code) != int:
        zip_code = input("Enter zip code:").strip()
        tries += 1
        if tries == 3:
            print("Too many invalid entries.\nExiting the program...")
            exit()

    complete_url = f"{base_url}zip={zip_code}&appid={api_key}"
    response = requests.get(complete_url)
    x = response.json()
    city_name = x["name"]
    lat = x['coord']['lat']
    lon = x['coord']['lon']

    if x["cod"] != "404":
        y = x["main"]
        current_temp = round(1.8 * (y["temp"]-273) + 32)
        feels_like = round(1.8 * (y["feels_like"]-273) + 32)
        current_pressure = round(y["pressure"]*.02953, 2)
        current_humidity = y["humidity"]
        z = x["weather"]
        wx_desc = z[0]["description"]

        print(f"Welcome,{call}\nThe current wx conditions in {city_name} are:")
        print(f"Temperature:\t\t{current_temp} F")
        print(f"Feels like:\t\t{feels_like} F")
        print(f"Pressure:\t\t{current_pressure} inches of mercury")
        print(f"Humidity:\t\t{current_humidity}%")
        print(f"Wx description:\t{wx_desc}")

    else:
        print(f"Zip code {zip_code} not found.")
