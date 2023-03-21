from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


app = Flask(__name__)

# Lire les fichiers CSV
meteo = pd.read_csv('meteo.csv', sep=';', index_col="Date", parse_dates=True)
meteo.index = pd.to_datetime(meteo.index, utc=True)
meteo.index = meteo.index.floor('D')
air = pd.read_csv('air.csv', sep=',', index_col="Date", parse_dates=True)
air.index = air.index.floor('D')



#########     choix colonnes meteo   ###########################
meteo = meteo[[ "Humidité", "Nom", "Température (°C)", "communes (name)", "communes (code)", "EPCI (name)", "department (name)", "region (name)"]]
meteo = meteo[meteo["region (name)"] == "Centre-Val de Loire"]
nb_lignes = meteo.shape[0]
print("Nombre de lignes pour la région Centre-Val de Loire :", nb_lignes)

#########       choix colonnes air #################
air = air[["lib_qual", "lib_zone", "conc_no2", "conc_so2", "conc_o3", "conc_pm10", "conc_pm25"]]
nb_lignes_air = air.shape[0]
print("Nombre de lignes pour la région Centre-Val de Loire :", nb_lignes_air)

#meteo_mean = meteo.groupby(["Date", "region (name)", "department (name)", "communes (name)"]).mean()
meteo_mean = meteo.groupby(["Date"]).mean()
meteo_mean= meteo_mean.reset_index()
print(meteo_mean.shape)

air_mean = air.groupby(["Date"]).mean()
air_mean= air_mean.reset_index()
print(air_mean.shape)

meteo_air = pd.merge(air_mean, meteo_mean, on="Date")
meteo_air = meteo_air.dropna(axis=0)
print(meteo_air.shape)


@app.route('/')
def page():
    return render_template('principalPage.html')


@app.route('/tableMeteo')
def tableMeteo():
    return render_template('tableMeteo.html', tables=[meteo_mean.head(250).to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    return render_template('tableAir.html', tables=[air.head(250).to_html()], titles=[''])

@app.route('/tableMeteoAir')
def tableMeteoAir():
    return render_template('tableMeteo.html', tables=[meteo_air.head(250).to_html()], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)
