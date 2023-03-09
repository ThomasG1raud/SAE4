from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


app = Flask(__name__)

# Lire les fichiers CSV
meteo = pd.read_csv('donneMeteo.csv',sep=',', index_col='Date', parse_dates=True)
#     meteo1=meteo.head()
air = pd.read_csv('openaq.csv',sep=',',index_col='Date', parse_dates=True)
#     air1=air.head()
#air.rename(index = {'Last Updated':'Date'}, inplace = True)
meteo_air = pd.merge(air, meteo, on='Date')

# Nettoyer les données

#     meteo.dropna(inplace=True)
print(meteo.columns)
# cols_to_drop_meteo = ['Pression station','Nébulosité couche nuageuse 2','Type de tendance barométrique.1']

# meteo.drop(columns=cols_to_drop_meteo, inplace=True)
# meteo.to_csv('donneMeteo.csv', index=False)



# #     air.dropna(inplace=True)
print(air.columns)
# cols_to_drop_air = ['Source Name', 'Country Code','Location']
# air.drop(columns=cols_to_drop_air, inplace=True)
# air.to_csv('openaq.csv', index=False)



# Fusionner les cadres de données
# merged_df = pd.merge(meteo, air, on='id')

@app.route('/')
def page():
    return render_template('principalPage.html')


@app.route('/tableMeteo')
def tableMeteo():
    meteo1=meteo.head()
    return render_template('tableMeteo.html', tables=[meteo1.to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    air1=air.head()
    return render_template('tableAir.html', tables=[air1.to_html()], titles=[''])

@app.route('/tableMeteoAir')
def tableMeteoAir():
    return render_template('tableMeteo.html', tables=[meteo_air.head().to_html()], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)
