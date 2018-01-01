import requests
import json
from pprint import pprint as pp
from datetime import datetime
import pytz
import tzlocal
from tzlocal import get_localzone
from src.json2xml import Json2xml
from geopy import geocoders
import os
from app.models import *
from app.sqlhelper import *


class WeatherClient(object):

    def __init__(self, appid, cityName):
        self._appid = appid
        self._cityName = cityName
        self._URI = 'http://api.openweathermap.org/data/2.5/forecast?appid='+self._appid+'&q='+self._cityName
        self._filename = "data" + "\\" + f"forecast{self._cityName}.json"


    @property
    def city(self):
        return self._city


    @property
    def weatherTimeSeries(self):
        return self._weatherTimeSeries


    def saveToFileasJSON(self):
        with open(self._filename, "w") as f:
            json.dump(self._json_object, f)


    def saveToFileasXML(self):
        xml = Json2xml(self._json_object)
        with open(self._filename, "wt") as f:
            f.write(xml.json2xml())


    def _setCity(self):
        jsonCity = self._json_object["city"]
        country = jsonCity["country"]
        longitude = jsonCity["coord"]["lon"]
        latitude = jsonCity["coord"]["lat"]

        self._city = City(self._cityName, country, latitude, longitude)


    def _setTimeSeries(self):
        self._weatherTimeSeries = []
        for item in self._json_object["list"]:
            self._weatherTimeSeries.append(WeatherDataPoint(item))


    def _save(self):
        # self.saveToFileasJSON()
        # self.saveToFileasXML()
        sql = sqlhelper()
        sql.insert_city(self._city)
        for item in self._weatherTimeSeries:
            sql.insert_weather_data(item)
            
        # print(sql.select_city(self._cityName))
        # print(sql.select_weather_data())
        

    def run(self):
        self._json_object = requests.get(self._URI).json()
        self._setCity()
        self._setTimeSeries()
        self._save()
        return self.weatherTimeSeries


    def display(self):
        title = str(self.city)
        for x in range(0, len(title)+1):
            if (x == len(title)):
                print("=")
            else:
                print("=", end = '')

        print(title)
        for x in range(0, len(title)+1):
            print("=", end = '')
        print(" ")

        for x in self._weatherTimeSeries:
            print(x)


def main():
    cities = ["Flagstaff", "Show Low", "Calgary", "Durango", "Denver"]
    for city in cities:
        client = WeatherClient("7d080362ace22e3a73b1d5789b4884e6", city)
        client.run()
        client.display()


if __name__ == '__main__':
    main()
