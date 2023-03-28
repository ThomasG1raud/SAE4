from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from datetime import datetime
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc

app = Flask(__name__)

##################  Lire les fichiers CSV   ##################
meteo2022 = pd.read_csv('meteo.csv', sep=';', index_col="Date", parse_dates=True)
meteo2022.index = pd.to_datetime(meteo2022.index, utc=True)
meteo2022.index = meteo2022.index.floor('D')

air = pd.read_csv('air.csv', sep=',', index_col="Date", parse_dates=True)
air.index = air.index.floor('D')

#########     choix colonnes meteo2022   ###########################
meteo2022 = meteo2022[["Humidité", "Nom", "Température (°C)", "communes (name)", "communes (code)", "EPCI (name)", "department (name)", "region (name)"]]
meteo2022 = meteo2022[meteo2022["region (name)"] == "Centre-Val de Loire"]
nb_lignes = meteo2022.shape[0]
print("Nombre de lignes meteo pour la région Centre-Val de Loire 2022 :", nb_lignes)

#########       choix colonnes air #################
air = air[["lib_qual", "lib_zone", "conc_no2", "conc_so2", "conc_o3", "conc_pm10", "conc_pm25"]]
nb_lignes_air = air.shape[0]
print("Nombre de lignes air pour la région Centre-Val de Loire :", nb_lignes_air)

########### Moyenne des données meteo pour un jour anne 2022 ##################
meteo_mean2022 = meteo2022.groupby(["Date"]).mean()
meteo_mean2022 = meteo_mean2022.reset_index()
print("meteo2022 moyenne : ", meteo_mean2022.shape)

########### Complétion air 2022 ##################

Dates = pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')
Dates = pd.DataFrame({'Date': Dates})
Dates["Date"] = pd.to_datetime(Dates["Date"], utc=True)
air = Dates.merge(air, on='Date', how='outer')

########### Moyenne des données air pour un jour anne 2022 ##################
air_mean = air.groupby(["Date"]).mean()
air_mean = air_mean.reset_index()
air_mean['conc_no2'] = air_mean['conc_no2'].interpolate(method='linear') # linear = L ; linear =
air_mean['conc_so2'] = air_mean['conc_so2'].interpolate(method='linear')
air_mean['conc_o3'] = air_mean['conc_o3'].interpolate(method='linear')
air_mean['conc_pm10'] = air_mean['conc_pm10'].interpolate(method='linear')
air_mean['conc_pm25'] = air_mean['conc_pm25'].interpolate(method='linear')
print("air moyenne :", air_mean.shape)

"""Utiliser les données de l'année précédente ou données """

########################## Merge  meteo et air region Centre val de loire ###########################
meteo_air = pd.merge(air_mean, meteo_mean2022, on="Date")
meteo_air['Température (°C)'] = meteo_air['Température (°C)'].round(2)
meteo_air['Humidité'] = meteo_air['Humidité'].round(2)
print("merge meteo air :", meteo_air.shape)

meteo_air['Date'] = meteo_air['Date'].dt.strftime('%Y-%m-%d')

############# graph 1 ################
"""
p = figure(title='Concentration en NO2 en fonction de la température', x_axis_label='Température (°C)', y_axis_label='Concentration en NO2')
p.circle(meteo_air['Température (°C)'], meteo_air['conc_no2'])

# Génération du code HTML et JavaScript pour le graphique
script, div = components(p)
"""
######################## Routes ########################################

@app.route('/')
def page():
    return render_template('principalPage.html')

@app.route('/tableMeteo')
def tableMeteo():
    return render_template('tableMeteo.html', tables=[meteo_mean2022.to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    return render_template('tableAir.html', tables=[air_mean.to_html()], titles=[''])

@app.route('/tableMeteoAir')
def tableMeteoAir():
    return render_template('tableMeteoAir.html', tables=[meteo_air.to_html()], titles=[''])
"""
@app.route('/graphique')
def graphique():
    return render_template('graphique.html', script=script, div=div)
"""

if __name__ == '__main__':
    app.run(debug=True)