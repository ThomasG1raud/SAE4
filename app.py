from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


app = Flask(__name__)

# Lire les fichiers CSV
meteo = pd.read_csv('meteo.csv',sep=';')

air = pd.read_csv('air.csv',sep=',')

#########     choix colonnes meteo   ###########################
meteo1 = meteo[["ID OMM station", "Date", "Humidité", "Nom", "Température (°C)", "Altitude", "communes (name)", "communes (code)", "EPCI (name)", "department (name)", "region (name)", "mois_de_l_annee"]]
df = meteo1[meteo1["region (name)"] == "Centre-Val de Loire"]
nb_lignes = df.shape[0]
print("Nombre de lignes pour la région Centre-Val de Loire :",nb_lignes)
# meteo1.to_csv('meteo1.csv', index=False)

#########       choix colonnes air #################
air1 = air[["lib_qual", "lib_zone", "code_no2", "code_so2", "code_o3", "code_pm10", "code_pm25", "conc_no2", "conc_so2", "conc_o3", "conc_pm10", "conc_pm25"]]
nb_lignes_air=air1.shape[0]
print("Nombre de lignes pour la région Centre-Val de Loire :",nb_lignes_air)
# air1.to_csv('air1.csv', index=False)

@app.route('/')
def page():
    return render_template('principalPage.html')


@app.route('/tableMeteo')
def tableMeteo():
    return render_template('tableMeteo.html', tables=[df.head().to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    return render_template('tableAir.html', tables=[air1.head().to_html()], titles=[''])

# @app.route('/tableMeteoAir')
# def tableMeteoAir():
#     return render_template('tableMeteo.html', tables=[meteo_air.to_html()], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)