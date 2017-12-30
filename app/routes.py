import os

from flask import Flask, request, render_template, redirect, url_for
from app import app
from app.weatherbot import *


@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('get_weather', city = request.form['city']))
    
    return render_template('welcome.html', title='Home')
    
@app.route('/weather/<city>')
def get_weather(city):
    app_id = '7d080362ace22e3a73b1d5789b4884e6'
    bot = WeatherClient(app_id, city)
    
    return render_template('weather.html', city=city, data=bot.run())
