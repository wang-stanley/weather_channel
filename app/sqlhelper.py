import sqlite3
from app.models import *
import json


class sqlhelper:
    
    def __init__(self):
        self._conn = sqlite3.connect('weatherapp.db')
        # self._conn = sqlite3.connect(':memory:')
        self._cursor = self.conn.cursor()
        
        # self._cursor.execute("""CREATE TABLE city (
        #             id integer,
        #             cityName text,
        #             lon real,
        #             lan real
        #             )""")
                    
        # self._cursor.execute("""CREATE TABLE weather_data_point (
        #             date text,
        #             temp real,
        #             description text,
        #             city_id integer
        #             )""")
    
    @property
    def conn(self):
        return self._conn
    
    
    @property
    def cursor(self):
        return self._cursor
     
    def insert_city(self, city):
        with self._conn:
            self._cursor.execute("INSERT INTO city VALUES (:id, :cityName, :lon, :lan)", {'id': 12345, 'cityName': city.name, 'lon': city.longitude, 'lan': city.latitude})
            
            
    def update_city(self, city):
        pass
    
    
    def delete_city(self, city):
        with self._conn:
            self._cursor.execute("DELETE from city WHERE cityName = :city",{'city': city.name})
    
            
    def select_city(self, name):
        self._cursor.execute("SELECT * FROM city WHERE cityName = :name", {"name": name})
        return self._cursor.fetchall()        
    
    
    # city = City('Chandler', 'United States', 33.31, -111.84)
    
    # insert_city(city)
    # print(select_city(city.name))
    
    # delete_city(city)
    # print(select_city(city.name))
    
    def insert_weather_data(self, wdp):
        with self._conn: 
            self._cursor.execute("INSERT INTO weather_data_point VALUES (:date, :temp, :description, :city_id)", 
            {'date': wdp.localTime, 'temp': wdp.temp, "description": wdp.weatherDescription, "city_id": 1})
            
    
    def select_weather_data(self):
        with self._conn: 
            self._cursor.execute("SELECT * FROM weather_data_point") 
            f = self._cursor.fetchall()
            # print(type(f))
            # for item in f:
            #     print(item)
            #     break
            return f
            
    # jsonData = json.dumps(
    #     {"dt": 1514613600,
    # 			"main": {
    # 				"temp": 282.19,
    # 				"temp_min": 276.997,
    # 				"temp_max": 282.19,
    # 				"pressure": 951.2,
    # 				"sea_level": 1034.89,
    # 				"grnd_level": 951.2,
    # 				"humidity": 59,
    # 				"temp_kf": 5.19
    # 			},
    # 			"weather": [{
    # 					"id": 800,
    # 					"main": "Clear",
    # 					"description": "clear sky",
    # 					"icon": "01n"
    # 				}
    # 			],
    # 			"clouds": {
    # 				"all": 0
    # 			},
    # 			"wind": {
    # 				"speed": 1.21,
    # 				"deg": 51.5025
    # 			},
    # 			"sys": {
    # 				"pod": "n"
    # 			},
    # 			"dt_txt": "2017-12-30 06:00:00"
    # 		}
    # 		)
    
    # print(type (jsonData) )
    # o = json.loads(jsonData)
    # print(type (o) ) 
    
    # wdp = WeatherDataPoint(o)
    # insert_weather_data(wdp)
    # print(select_weather_data())
    
    

        