import os

from flask import Flask, request, render_template, redirect, url_for
from app import app
from app.weatherbot import *
from app.sqlhelper import *

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('get_weather', city = request.form['city']))
    
    return render_template('welcome.html', title='Home')
    
@app.route('/weather/<city>')
def get_weather(city):
    # bot = WeatherClient("7d080362ace22e3a73b1d5789b4884e6", city)
    # bot.run()
    helper = sqlhelper()
    data=helper.select_weather_data()
    return render_template('weather.html', city=city, data=data)
