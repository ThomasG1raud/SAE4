from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


app = Flask(__name__)

# Lire les fichiers CSV
meteo = pd.read_csv('donneMeteo.csv',sep=',', index_col='Date', parse_dates=True)
deplacementCol1 = meteo.pop('department (name)')
meteo.insert(0, 'department (name)', deplacementCol1)
deplacementCol2 = meteo.pop('region (name)')
meteo.insert(1, 'region (name)', deplacementCol1)
meteo1=meteo.head()
air = pd.read_csv('openaq.csv',sep=',',index_col='Date', parse_dates=True)
air1=air.head()

air1_pivot = air1.pivot(index=['Date','City', 'Coordinates', 'Unit', 'Value','Country Label'], columns='Pollutant', values='Value')
air1_pivot = air1_pivot.rename(columns={'O3': 'O3 (µg/m³)', 'PM10': 'PM10 (µg/m³)', 'NO2': 'NO2 (µg/m³)', 'PM2.5': 'PM2.5 (µg/m³)'})

meteo_air = pd.concat([air, meteo]) # a refaire
#meteo_air = pd.concat(air, meteo, on='Date')
print(meteo.columns)
print(air.columns)

@app.route('/')
def page():
    return render_template('principalPage.html')


@app.route('/tableMeteo')
def tableMeteo():
    return render_template('tableMeteo.html', tables=[meteo1.to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    return render_template('tableAir.html', tables=[air1.to_html()], titles=[''])

# @app.route('/tableMeteoAir') # a refaire
# def tableMeteoAir():
#     return render_template('tableMeteo.html', tables=[meteo_air.head().to_html()], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)