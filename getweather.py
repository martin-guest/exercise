#!/usr/bin/env python3
import pyowm
import os

api_key = os.environ['OPENWEATHER_API_KEY']
city = os.environ['CITY_NAME']

owm = pyowm.OWM(api_key)  # You MUST provide a valid API key

observation = owm.weather_at_place(city)
w = observation.get_weather()

description = w.get_detailed_status()
temp = w.get_temperature(unit='celsius')['temp']
humidity = w.get_humidity()

print('source=openweathermap, city="%s", description="%s", temp=%s, humidity=%s' % (city,description,temp,humidity))
