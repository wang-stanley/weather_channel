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


class WeatherDataPoint(object):
    def __init__(self, item):
        dt = datetime.fromtimestamp(item["dt"])
        tz = get_localzone()
        self._localTime = dt.astimezone(tz)


        self._dt = item["dt"]
        self._temp = self._Fahrenheit(item["main"]["temp"])
        self._min_temp = self._Fahrenheit(item["main"]["temp_min"])
        self._max_temp = self._Fahrenheit(item["main"]["temp_max"])

    @property
    def dt(self):
        return self._dt


    @property
    def temp(self):
        return self._temp


    @property
    def min_temp(self):
        return self._min_temp


    @property
    def max_temp(self):
        return self._max_temp


    def _Fahrenheit(self, temp_k):
        temp_f = 1.8 * (temp_k - 273.15) + 32
        return temp_f

    def __str__(self):
        return("{0}\t{1:6.2f}\t{2:6.2f}\t{3:6.2f}".format(self._localTime.strftime("%Y/%m/%d, %I:%M:%p"), self._temp, self._min_temp, self._max_temp))


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
        self.saveToFileasJSON()
        self.saveToFileasXML()


    def run(self):
        self._json_object = requests.get(self._URI).json()
        self.saveToFileasJSON()
        self._setCity()
        self._setTimeSeries()
        return self._weatherTimeSeries


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
