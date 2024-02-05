#!/bin/python3
# Get wx for zip code

import configparser
from datetime import datetime, timezone
import os
import sys

import requests

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "credentials.txt")


def deg_to_compass(deg):
    """
    Converts degrees to N, NE, SW, etc.
    :param deg: Double denoting degrees
    :return: string denoting compass direction
    """

    val = int((deg / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW",
           "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


api_key = "NULL"
config = configparser.ConfigParser()
try:
    config.read(config_path)
    api_key = config['DEFAULT']['api_key']
except KeyError:
    print(
        "You must first create a credentials file named credentials.txt that adheres to the following format:\n")
    print("[DEFAULT]\napi_key=YOURAPIKEYHERE")

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

call = input()  # capture BPQ call sign that is sent
print(f"Hello, {call}\n")

zip_code = None
tries = 0
if api_key != "NULL":
    while zip_code is None or len(zip_code) != 5 and type(zip_code) != int:
        zip_code = input("Enter zip code:")
        zip_code = zip_code.strip()
        tries += 1
        if tries == 3:
            print("Too many invalid entries.\nExiting the program...")
            exit()

    complete_url = f"{base_url}zip={zip_code}&appid={api_key}&units=imperial"
    response = requests.get(complete_url)
    x = response.json()
    response_code = x["cod"]

    if response_code == 401:
        print("Error: Unauthorized OpenWeatherAPI access. Please check your API key and ensure it is active.")
        sys.exit()

    city_name = None
    try:
        city_name = x["name"]
    except KeyError:
        # Couldn't get city
        print("Sorry, couldn't find information for that zip code. Exiting.")
        exit()
    lat = x['coord']['lat']
    lon = x['coord']['lon']

    if response_code == 200:
        timestamp = datetime.utcfromtimestamp(x["dt"])
        timestamp = timestamp.replace(tzinfo=timezone.utc).astimezone(
            tz=None).strftime("%Y-%m-%d %I:%M %p")

        main = x["main"]
        wind = x["wind"]
        current_temp = main["temp"]
        feels_like = main["feels_like"]
        current_pressure = round(main["pressure"] * .02953, 2)
        current_humidity = main["humidity"]
        wind_speed = wind["speed"]
        wind_degree = wind["deg"]
        wind_dir = deg_to_compass(wind_degree)
        z = x["weather"]
        wx_desc = z[0]["description"]

        # Try to get wind gust speed, if available
        wind_gust = None
        try:
            wind_gust = wind["gust"]
        except KeyError:
            # No wind gust measurement
            pass

        # Try to get rain & snow measurements, if available
        rain = None
        snow = None
        rain_1h = None
        rain_3h = None
        snow_1h = None
        snow_3h = None

        try:
            rain = x["rain"]
            rain_1h = rain["1h"]
            rain_3h = rain["3h"]
        except KeyError:
            # Must not have rained
            pass
        try:
            snow = x["snow"]
            snow_1h = snow["1h"]
            snow_3h = snow["3h"]
        except KeyError:
            # Must not have snowed
            pass

        print(
            f"The current wx conditions in {city_name} as of {timestamp} are:")
        print(f"Temperature:\t\t{current_temp} F")
        print(f"Feels like:\t\t{feels_like} F")
        print(f"Pressure:\t\t{current_pressure} inches of mercury")
        print(f"Humidity:\t\t{current_humidity}%")
        print(
            f"Wind speed is {wind_speed} MPH from the {wind_dir}.")

        if wind_gust:
            print(f"Wind gusting up to {wind_gust} MPH.")

        if rain:
            print(
                f"It has rained {round(rain_1h * .0393701), 2} inches in the "
                f"past hour,\n and {round(rain_3h * .0393701), 2} "
                f"inches in the past 3 hours.")

        if snow:
            print(
                f"It has snowed {round(snow_1h * .0393701), 2} inches in the "
                f"past hour,\n and {round(snow_3h * .0393701), 2} "
                f"inches in the past 3 hours.")

        print(f"Wx description:\t{wx_desc}")

    else:
        print(f"Zip code {zip_code} not found.")
