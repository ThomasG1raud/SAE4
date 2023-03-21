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
meteo = meteo[["ID OMM station", "Humidité", "Nom", "Température (°C)", "Altitude", "communes (name)", "communes (code)", "EPCI (name)", "department (name)", "region (name)", "mois_de_l_annee"]]
meteo = meteo[meteo["region (name)"] == "Centre-Val de Loire"]
nb_lignes = meteo.shape[0]
print("Nombre de lignes pour la région Centre-Val de Loire :", nb_lignes)

#########       choix colonnes air #################
air = air[["lib_qual", "lib_zone", "code_no2", "code_so2", "code_o3", "code_pm10", "code_pm25", "conc_no2", "conc_so2", "conc_o3", "conc_pm10", "conc_pm25"]]
nb_lignes_air = air.shape[0]
print("Nombre de lignes pour la région Centre-Val de Loire :", nb_lignes_air)


meteo_air = pd.merge(air, meteo, on="Date")
meteo_air = meteo_air.dropna(axis=0)

@app.route('/')
def page():
    return render_template('principalPage.html')


@app.route('/tableMeteo')
def tableMeteo():
    return render_template('tableMeteo.html', tables=[meteo.tail(250).to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    return render_template('tableAir.html', tables=[air.tail(250).to_html()], titles=[''])

@app.route('/tableMeteoAir')
def tableMeteoAir():
    return render_template('tableMeteo.html', tables=[meteo_air.tail(250).to_html()], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)
