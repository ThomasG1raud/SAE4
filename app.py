from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


app = Flask(__name__)

# Lire les fichiers CSV
meteo = pd.read_csv('meteo.csv',sep=';')
# meteo.dropna(inplace=True)
meteo1=meteo.head()

air = pd.read_csv('Air.csv',sep=',')
air.dropna(inplace=True)
air1=air.head()


################  chagements de pace de colonne ####################
# deplacementCol1 = meteo.pop('department (name)')
# meteo.insert(0, 'department (name)', deplacementCol1)
# deplacementCol2 = meteo.pop('region (name)')
#meteo.insert(1, 'region (name)', deplacementCol1)


##########   changement de données colonne en colonnes


# concatener les deux tables air et meteo ?
# meteo_air = pd.concat([meteo, air1_pivot], axis=1, join='inner')
# meteo_air.to_csv('meteo_air.csv', index=False)
# meteo_air = pd.concat([meteo, air1_pivot], axis=1)


#########     effacer colonnes meteo   ###########################
print(meteo.columns)
# cols_to_drop_meteo = ['Pression station','Nébulosité couche nuageuse 2','Type de tendance barométrique.1']
# meteo.drop(columns=cols_to_drop_meteo, inplace=True)
# meteo.to_csv('donneMeteo.csv', index=False)


#########       effacer colonnes air #################
print(air.columns)
# cols_to_drop_air = ['Source Name', 'Country Code','Location']
# air.drop(columns=cols_to_drop_air, inplace=True)
# air.to_csv('openaq.csv', index=False)


@app.route('/')
def page():
    return render_template('principalPage.html')


@app.route('/tableMeteo')
def tableMeteo():
    return render_template('tableMeteo.html', tables=[meteo1.to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    return render_template('tableAir.html', tables=[air1.to_html()], titles=[''])

# @app.route('/tableMeteoAir')
# def tableMeteoAir():
#     return render_template('tableMeteo.html', tables=[meteo_air.to_html()], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)