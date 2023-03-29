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
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.models import ColumnDataSource, HoverTool


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


p1 = figure(title='Température et humidité', x_axis_label='Température (°C)', y_axis_label='Humidité')
p1.circle(meteo_air['Température (°C)'], meteo_air['Humidité'])

# Génération du code HTML et JavaScript pour le graphique
script1, div1 = components(p1)



############# graph 2 ################
meteo_air['Date'] = pd.to_datetime(meteo_air['Date'], format='%Y-%m-%d')
meteo_air['Month'] = meteo_air['Date'].dt.month_name()

p2 = figure(title='Température en fonction du temps', x_axis_label='Date', y_axis_label='Température (°C)')
p2.line(meteo_air['Month'].index, meteo_air['Température (°C)'])

# Génération du code HTML et JavaScript pour le graphique
script2, div2 = components(p2)

############# graph 3 ################

p3 = figure(title='Humidité en fonction du temps', x_axis_label='Date', y_axis_label='Humidité')
p3.line(meteo_air['Month'].index, meteo_air['Humidité'])

# Génération du code HTML et JavaScript pour le graphique
script3, div3 = components(p3)

############# graph 4 ################

p4 = figure(title='Concentration en NO2 en fonction de la température', x_axis_label='Température (°C)', y_axis_label='Concentration en NO2')
p4.circle(meteo_air['Température (°C)'], meteo_air['conc_no2'])

# Génération du code HTML et JavaScript pour le graphique
script4, div4 = components(p4)


############# graph 5 ################

p5 = figure(x_axis_label="Température (°C)", y_axis_label="Concentration", title="Les différentes concentration en fonction de la température")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_no2"], color="red", legend_label="NO2")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_o3"], color="blue", legend_label="O3")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_so2"], color="orange", legend_label="SO2")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_pm10"], color="green", legend_label="PM10")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_pm25"], color="yellow", legend_label="PM25")

p5.legend.location = "top_left"
script5, div5 = components(p5)

############# graph 6################

p6 = figure(x_axis_label="Humidité", y_axis_label="Concentration", title="Les différentes concentration en fonction de l'humidité")
p6.circle(meteo_air["Humidité"], meteo_air["conc_no2"], color="red", legend_label="NO2")
p6.circle(meteo_air["Humidité"], meteo_air["conc_o3"], color="blue", legend_label="O3")
p6.circle(meteo_air["Humidité"], meteo_air["conc_so2"], color="orange", legend_label="SO2")
p6.circle(meteo_air["Humidité"], meteo_air["conc_pm10"], color="green", legend_label="PM10")
p6.circle(meteo_air["Humidité"], meteo_air["conc_pm25"], color="yellow", legend_label="PM25")

p6.legend.location = "top_left"
script6, div6 = components(p6)

############# graph 7 ################

p7 = figure(title='Concentration en molécules dans l air', x_axis_label='Molécules', y_axis_label='Concentration')
p7.vbar(x=air_mean.index, top=air_mean['conc_no2'], width=0.9, color="blue", legend_label="NO2")
p7.vbar(x=air_mean.index, top=air_mean['conc_o3'], width=0.9, color="orange", legend_label="O3")
p7.vbar(x=air_mean.index, top=air_mean['conc_pm10'], width=0.9, color="green", legend_label="PM10")
p7.vbar(x=air_mean.index, top=air_mean['conc_pm25'], width=0.9, color="yellow", legend_label="PM25")
p7.vbar(x=air_mean.index, top=air_mean['conc_so2'], width=0.9, color="purple", legend_label="SO2")

# Génération du code HTML et JavaScript pour le graphique
script7, div7 = components(p7)







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

@app.route('/graphique')
def graphique():
    return render_template('graphique.html', script=script1, div=div1, script2=script2, div2=div2, script3=script3, div3=div3, script4=script4, div4=div4, script5=script5, div5=div5, script6=script6, div6=div6, script7=script7, div7=div7)

if __name__ == '__main__':
    app.run(debug=True)