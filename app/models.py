import requests, pprint, sys, json, pytz, tzlocal, time
from tzlocal import get_localzone
from datetime import datetime
from src.json2xml import Json2xml

class City(object):
    def __init__(self, name, country, latitude, longitude):
        self._name = name
        self._country = country
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self):
        return self._name


    @property
    def country(self):
        return self._country


    @property
    def latitude(self):
        return self._latitude


    @property
    def longitude(self):
        return self._longitude

    def __str__(self):
        return "{0.name}, {0.country}, (lat = {0.latitude}, lon = {0.longitude})".format(self)


class WeatherDataPoint:

    """  Weather Forecast Data Point """
	
    def __init__(self, jsonWeatherItem): 
        dt = datetime.fromtimestamp(jsonWeatherItem["dt"]) 
        tz = pytz.timezone("US/Arizona")
        self._localTime = dt.astimezone(tz)

        main = jsonWeatherItem["main"]
        self._temp = self._Fahrenheit(main["temp"]) 
		
        weather = jsonWeatherItem["weather"]
        self._weatherDescription = weather[0]["description"]

		
    @property
    def localTime(self):
        return self._localTime

		
    @property	
    def temp(self):
        return self._temp
		
		
    @property	
    def weatherDescription(self):
        return self._weatherDescription
		

    def _Fahrenheit(self, temp_k):
        temp_c = temp_k - 273.15
        temp_f =  temp_c * 9/5 + 32
        return temp_f
		
		
    def __str__(self):
	        return("\t{0}\t{1:8.0f}\t{2}".format(self.localTime.strftime("%a %m-%d-%Y %I:%M:%S %p %Z"), self.temp, self.weatherDescription))