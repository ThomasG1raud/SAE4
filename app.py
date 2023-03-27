from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from datetime import datetime
from bokeh.models import Select
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Select
from bokeh.layouts import column, row
from bokeh.embed import components
from bokeh.io import output_file, show
from bokeh.palettes import Category10
from bokeh.plotting import figure, output_file, show
from bokeh.models.callbacks import CustomJS

app = Flask(__name__)

##################  Lire les fichiers CSV   ##################
meteo2022 = pd.read_csv('meteo2022.csv', sep=';', index_col="Date", parse_dates=True)
meteo2022.index = pd.to_datetime(meteo2022.index, utc=True)
meteo2022.index = meteo2022.index.floor('D')

air = pd.read_csv('air.csv', sep=',', index_col="Date", parse_dates=True)
air.index = air.index.floor('D')

#########     choix colonnes meteo2022   ###########################
meteo2022 = meteo2022[[ "Humidité", "Nom", "Température (°C)", "communes (name)", "communes (code)", "EPCI (name)", "department (name)", "region (name)"]]
meteo2022 = meteo2022[meteo2022["region (name)"] == "Centre-Val de Loire"]
nb_lignes = meteo2022.shape[0]
print("Nombre de lignes meteo pour la région Centre-Val de Loire 2022 :", nb_lignes)

#########       choix colonnes air #################
air = air[["lib_qual", "lib_zone", "conc_no2", "conc_so2", "conc_o3", "conc_pm10", "conc_pm25"]]
nb_lignes_air = air.shape[0]
print("Nombre de lignes air pour la région Centre-Val de Loire :", nb_lignes_air)


########### Moyenne des données meteo pour un jour anne 2022 ##################
meteo_mean2022 = meteo2022.groupby(["Date"]).mean()
meteo_mean2022= meteo_mean2022.reset_index()
print("meteo2022 moyenne : ",meteo_mean2022.shape)

########### Moyenne des données meteo par commune et par mois ##################

########### Moyenne des données air pour un jour anne 2021 ##################
air_mean = air.groupby(["Date"]).mean()
air_mean= air_mean.reset_index()
print("air moyenne :",air_mean.shape)

########################## Merge  meteo et air region Centre val de loire ###########################
meteo_air = pd.merge(air_mean, meteo_mean2022, on="Date")
meteo_air = meteo_air.dropna(axis=0)
print("merge meteo air :",meteo_air.shape)

meteo_air['Date'] = meteo_air['Date'].dt.strftime('%Y-%m-%d')
meteo_air['Date'] = pd.to_datetime(meteo_air['Date'])

meteo_air['Month'] = meteo_air['Date'].dt.month_name()
print(meteo_air.tail(2))

meteo_air_mean = meteo_air.groupby(["Month"]).mean()
meteo_air_mean= meteo_air_mean.reset_index()


source = ColumnDataSource(meteo_air)

months = meteo_air['Month'].unique().tolist()
month_select = Select(title="Mois", value=months[0], options=months)

# # Créer un graphique avec les données initiales
# p = figure(x_axis_type="datetime", title="Concentration en polluants atmosphériques")
# p.line('Date', 'conc_no2', source=source, line_width=2, legend_label="NO2")
# p.line('Date', 'conc_so2', source=source, line_width=2, legend_label="SO2", color='orange')
# p.line('Date', 'conc_o3', source=source, line_width=2, legend_label="O3", color='green')
# p.line('Date', 'conc_pm10', source=source, line_width=2, legend_label="PM10", color='red')
# p.line('Date', 'conc_pm25', source=source, line_width=2, legend_label="PM2.5", color='purple')

# #  fonctionpour mettre à jour les données en fonction du mois 
# def update_data(attrname, old, new):
#     print("Fonction de rappel appelée")
#     selected_month = month_select.value
#     filtered_data = meteo_air[meteo_air['Month'] == selected_month]
#     source.data = ColumnDataSource.from_df(filtered_data).data

# month_select.on_change('value', update_data)
# layout = row(p, month_select)
# show(layout)
# script, div = components(layout)


######################## Routes ######################################## 

@app.route('/')
def page():
    return render_template('principalPage.html')

@app.route('/tableMeteo')
def tableMeteo():
    return render_template('tableMeteo.html', tables=[meteo2022.tail(250).to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    return render_template('tableAir.html', tables=[air.head(250).to_html()], titles=[''])

@app.route('/tableMeteoAir')
def tableMeteoAir():
    return render_template('tableMeteoAir.html', tables=[meteo_air.head(250).to_html()], titles=[''])

@app.route('/graphique')
def graphique():
    return render_template('graphique.html')


if __name__ == '__main__':
    app.run(debug=True)
