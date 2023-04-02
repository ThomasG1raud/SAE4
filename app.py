from flask import Flask, render_template, url_for
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from datetime import datetime
from bokeh.plotting import figure
from bokeh.embed import components,server_document
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import column, row
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.models.widgets import Select
import folium 

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
meteo_air['Date'] = pd.to_datetime(meteo_air['Date'], format='%Y-%m-%d')
meteo_air['Month'] = meteo_air['Date'].dt.month_name()
meteo_air_mean = meteo_air.groupby(['Month']).mean()
# meteo_air_mean = meteo_air_mean.reset_index()


ordre = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
sns.barplot(x=meteo_air_mean.index ,y='Température (°C)', data=meteo_air_mean,order=ordre)
plt.xlabel('Month')
plt.xticks(rotation=90)
plt.ylabel('Température (°C)')
plt.title('Température par mois')
plt.savefig('static/images/graph2.png')


############# graph 2 ################
source = ColumnDataSource(meteo_air)
#temperature
p2 = figure(title="Temperature par rapport au temps", x_axis_label='Date', y_axis_label='Température (°C)', x_axis_type='datetime')
p2.line('Date', 'Température (°C)', source=source)
#humidité
p3 = figure(title="Humidité par rapport au temps", x_axis_label='Date', y_axis_label='Humidité', x_axis_type='datetime')
p3.line('Date', 'Humidité', source=source)
layouts = row(p2, p3)
# Génération du code HTML et JavaScript pour le graphique
scriptMeteo, divMeteo = components(layouts)

############# graph 3 ################


############# graph 5 ################

p5 = figure(x_axis_label="Température (°C)", y_axis_label="Concentration", title="Les différentes concentration en fonction de la température")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_no2"], color="red", legend_label="NO2")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_o3"], color="blue", legend_label="O3")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_so2"], color="orange", legend_label="SO2")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_pm10"], color="green", legend_label="PM10")
p5.circle(meteo_air["Température (°C)"], meteo_air["conc_pm25"], color="yellow", legend_label="PM25")

p5.legend.location = "top_left"
############# graph 6################

p6 = figure(x_axis_label="Humidité", y_axis_label="Concentration", title="Les différentes concentration en fonction de l'humidité")
p6.circle(meteo_air["Humidité"], meteo_air["conc_no2"], color="red", legend_label="NO2")
p6.circle(meteo_air["Humidité"], meteo_air["conc_o3"], color="blue", legend_label="O3")
p6.circle(meteo_air["Humidité"], meteo_air["conc_so2"], color="orange", legend_label="SO2")
p6.circle(meteo_air["Humidité"], meteo_air["conc_pm10"], color="green", legend_label="PM10")
p6.circle(meteo_air["Humidité"], meteo_air["conc_pm25"], color="yellow", legend_label="PM25")

p6.legend.location = "top_left"


# je veut p5 et p6 a cote 
layoutsConcT = row(p5,p6)
script6, div6 = components(layoutsConcT)

############# graph 7 ################

# p7 = figure(title='Concentration en molécules dans l air', x_axis_label='Molécules', y_axis_label='Concentration')
# p7.vbar(x=air_mean.index, top=air_mean['conc_no2'], width=0.9, color="blue", legend_label="NO2")
# p7.vbar(x=air_mean.index, top=air_mean['conc_o3'], width=0.9, color="orange", legend_label="O3")
# p7.vbar(x=air_mean.index, top=air_mean['conc_pm10'], width=0.9, color="green", legend_label="PM10")
# p7.vbar(x=air_mean.index, top=air_mean['conc_pm25'], width=0.9, color="yellow", legend_label="PM25")
# p7.vbar(x=air_mean.index, top=air_mean['conc_so2'], width=0.9, color="purple", legend_label="SO2")

# # Génération du code HTML et JavaScript pour le graphique
# scriptMol, divMol= components(p7)

############# graph 8 ################
source = ColumnDataSource(meteo_air)
# months = meteo_air['Month'].unique().tolist()
# month_select = Select(title="Mois", value=months[0], options=months)

# Créer un graphique avec les données initiales
p8 = figure(x_axis_type="datetime", title="Concentration en polluants atmosphériques")
p8.line('Date', 'conc_no2', source=source, line_width=2, legend_label="NO2")
p8.line('Date', 'conc_so2', source=source, line_width=2, legend_label="SO2", color='orange')
p8.line('Date', 'conc_o3', source=source, line_width=2, legend_label="O3", color='green')
p8.line('Date', 'conc_pm10', source=source, line_width=2, legend_label="PM10", color='red')
p8.line('Date', 'conc_pm25', source=source, line_width=2, legend_label="PM2.5", color='purple')

# #  fonctionpour mettre à jour les données en fonction du mois
# def update_data(attrname, old, new):
#     print("Fonction de rappel appelée")
#     selected_month = month_select.value
#     filtered_data = meteo_air[meteo_air['Month'] == selected_month]
#     source.data = ColumnDataSource.from_df(filtered_data).data

# month_select.on_change('value', update_data)
# layout = row(p8, month_select)
# legend
p8.legend.location = "top_left"
p8.legend.click_policy="hide"


script8, div8 = components(p8)

############# graph 9 ################
#concentrations par rapport a la température
meteo_air_janvier = meteo_air[meteo_air["Month"] == "January"]
meteo_air_janvier = meteo_air_janvier.dropna(axis=0)
meteo_air_janvier = meteo_air_janvier.reset_index()

meteo_air_janvier = meteo_air_janvier.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_janvier)
p = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de janvier")
p.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
p.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
p.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
p.line(x="Température (°C)", y="conc_o3", source=source,legend_label="03", line_width=2, color="green", alpha=0.5)
p.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
p.line(x="Température (°C)", y="conc_so2", source=source, legend_label="so2",line_width=2, color="yellow", alpha=0.5)
p.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
p.line(x="Température (°C)", y="conc_pm10", source=source, legend_label="pm10",line_width=2, color="blue", alpha=0.5)
p.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
p.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
p.legend.location = "top_left"
p.legend.click_policy="hide"


scriptConcJ, divConcJ = components(p)

#pour le mois de fevrier
meteo_air_fevrier = meteo_air[meteo_air["Month"] == "February"]
meteo_air_fevrier = meteo_air_fevrier.dropna(axis=0)
meteo_air_fevrier = meteo_air_fevrier.reset_index()

meteo_air_fevrier = meteo_air_fevrier.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_fevrier)
pF = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de fevrier")
pF.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pF.line(x="Température (°C)", y="conc_no2", source=source,legend_label="no2", line_width=2, color="red", alpha=0.5)
pF.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pF.line(x="Température (°C)", y="conc_o3", source=source,legend_label="o3", line_width=2, color="green", alpha=0.5)
pF.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pF.line(x="Température (°C)", y="conc_so2", source=source, legend_label="so2",line_width=2, color="yellow", alpha=0.5)
pF.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pF.line(x="Température (°C)", y="conc_pm10", source=source, legend_label="pm10",line_width=2, color="blue", alpha=0.5)
pF.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pF.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
pF.legend.location = "top_left"
pF.legend.click_policy="hide"

scritConcFev, divConcFev = components(pF)

#pour le mois de mars
meteo_air_mars = meteo_air[meteo_air["Month"] == "March"]
meteo_air_mars = meteo_air_mars.dropna(axis=0)
meteo_air_mars = meteo_air_mars.reset_index()

meteo_air_mars = meteo_air_mars.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_mars)
p3 = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de mars")
p3.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
p3.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
p3.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
p3.line(x="Température (°C)", y="conc_o3", source=source,legend_label="o3", line_width=2, color="green", alpha=0.5)
p3.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
p3.line(x="Température (°C)", y="conc_so2", source=source,legend_label="so2", line_width=2, color="yellow", alpha=0.5)
p3.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
p3.line(x="Température (°C)", y="conc_pm10", source=source, legend_label="pm10",line_width=2, color="blue", alpha=0.5)
p3.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
p3.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
p3.legend.location = "top_left"
p3.legend.click_policy="hide"


scriptConcMars, divConcMars = components(p3)

#pour le mois d'avril
meteo_air_avril = meteo_air[meteo_air["Month"] == "April"]
meteo_air_avril = meteo_air_avril.dropna(axis=0)
meteo_air_avril = meteo_air_avril.reset_index()

meteo_air_avril = meteo_air_avril.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_avril)
pA = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois d'avril")
pA.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pA.line(x="Température (°C)", y="conc_no2", source=source,legend_label="no2", line_width=2, color="red", alpha=0.5)
pA.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pA.line(x="Température (°C)", y="conc_o3", source=source, legend_label="o3",line_width=2, color="green", alpha=0.5)
pA.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pA.line(x="Température (°C)", y="conc_so2", source=source, legend_label="so2",line_width=2, color="yellow", alpha=0.5)
pA.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pA.line(x="Température (°C)", y="conc_pm10", source=source,legend_label="pm10", line_width=2, color="blue", alpha=0.5)
pA.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pA.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
pA.legend.location = "top_left"
pA.legend.click_policy="hide"


scriptConcAvril, divConcAvril = components(pA)

#pour le mois suivants
meteo_air_mai = meteo_air[meteo_air["Month"] == "May"]
meteo_air_mai = meteo_air_mai.dropna(axis=0)
meteo_air_mai = meteo_air_mai.reset_index()

meteo_air_mai = meteo_air_mai.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_mai)
pM = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de mai")
pM.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pM.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
pM.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pM.line(x="Température (°C)", y="conc_o3", source=source, legend_label="o3",line_width=2, color="green", alpha=0.5)
pM.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pM.line(x="Température (°C)", y="conc_so2", source=source, legend_label="so2",line_width=2, color="yellow", alpha=0.5)
pM.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pM.line(x="Température (°C)", y="conc_pm10", source=source,legend_label="pm10", line_width=2, color="blue", alpha=0.5)
pM.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pM.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
pM.legend.location = "top_left"
pM.legend.click_policy="hide"


scriptConcMai, divConcMai = components(pM)

#pour le mois de juin
meteo_air_juin = meteo_air[meteo_air["Month"] == "June"]
meteo_air_juin = meteo_air_juin.dropna(axis=0)
meteo_air_juin = meteo_air_juin.reset_index()

meteo_air_juin = meteo_air_juin.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_juin)
pJuin = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de juin")
pJuin.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pJuin.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
pJuin.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pJuin.line(x="Température (°C)", y="conc_o3", source=source, legend_label="o3",line_width=2, color="green", alpha=0.5)
pJuin.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pJuin.line(x="Température (°C)", y="conc_so2", source=source,legend_label="so2", line_width=2, color="yellow", alpha=0.5)
pJuin.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pJuin.line(x="Température (°C)", y="conc_pm10", source=source,legend_label="pm10", line_width=2, color="blue", alpha=0.5)
pJuin.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pJuin.line(x="Température (°C)", y="conc_pm25", source=source,legend_label="pm25", line_width=2, color="orange", alpha=0.5)

# legend
pJuin.legend.location = "top_left"
pJuin.legend.click_policy="hide"


scriptConcJuin, divConcJuin = components(pJuin)

#pour le mois de juillet
meteo_air_juillet = meteo_air[meteo_air["Month"] == "July"]
meteo_air_juillet = meteo_air_juillet.dropna(axis=0)
meteo_air_juillet = meteo_air_juillet.reset_index()

meteo_air_juillet = meteo_air_juillet.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_juillet)
pJu = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de juillet")
pJu.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pJu.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
pJu.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pJu.line(x="Température (°C)", y="conc_o3", source=source,legend_label="o3", line_width=2, color="green", alpha=0.5)
pJu.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pJu.line(x="Température (°C)", y="conc_so2", source=source, legend_label="so2",line_width=2, color="yellow", alpha=0.5)
pJu.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pJu.line(x="Température (°C)", y="conc_pm10", source=source, legend_label="pm10",line_width=2, color="blue", alpha=0.5)
pJu.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pJu.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
pJu.legend.location = "top_left"
pJu.legend.click_policy="hide"


scriptConcJu, divConcJu = components(pJu)

#pour le mois d'août
meteo_air_aout = meteo_air[meteo_air["Month"] == "August"]
meteo_air_aout = meteo_air_aout.dropna(axis=0)
meteo_air_aout = meteo_air_aout.reset_index()

meteo_air_aout = meteo_air_aout.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_aout)
pAo = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois d'août")
pAo.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pAo.line(x="Température (°C)", y="conc_no2", source=source,legend_label="no2", line_width=2, color="red", alpha=0.5)
pAo.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pAo.line(x="Température (°C)", y="conc_o3", source=source, legend_label="o3",line_width=2, color="green", alpha=0.5)
pAo.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pAo.line(x="Température (°C)", y="conc_so2", source=source,legend_label="so2", line_width=2, color="yellow", alpha=0.5)
pAo.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pAo.line(x="Température (°C)", y="conc_pm10", source=source, legend_label="pm10",line_width=2, color="blue", alpha=0.5)
pAo.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pAo.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
pAo.legend.location = "top_left"
pAo.legend.click_policy="hide"

scriptConcAo, divConcAo = components(pAo)

#pour le mois de septembre
meteo_air_septembre = meteo_air[meteo_air["Month"] == "September"]
meteo_air_septembre = meteo_air_septembre.dropna(axis=0)
meteo_air_septembre = meteo_air_septembre.reset_index()

meteo_air_septembre = meteo_air_septembre.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_septembre)
pS = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de septembre")
pS.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pS.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
pS.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pS.line(x="Température (°C)", y="conc_o3", source=source, legend_label="o3",line_width=2, color="green", alpha=0.5)
pS.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pS.line(x="Température (°C)", y="conc_so2", source=source, legend_label="so2",line_width=2, color="yellow", alpha=0.5)
pS.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pS.line(x="Température (°C)", y="conc_pm10", source=source, legend_label="pm10",line_width=2, color="blue", alpha=0.5)
pS.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pS.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

#legend
pS.legend.location = "top_left"
pS.legend.click_policy="hide"


scriptConcS, divConcS = components(pS)

#pour le mois d'octobre
meteo_air_octobre = meteo_air[meteo_air["Month"] == "October"]
meteo_air_octobre = meteo_air_octobre.dropna(axis=0)
meteo_air_octobre = meteo_air_octobre.reset_index()

meteo_air_octobre = meteo_air_octobre.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_octobre)
pO = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois d'octobre")
pO.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pO.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
pO.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pO.line(x="Température (°C)", y="conc_o3", source=source, legend_label="o3",line_width=2, color="green", alpha=0.5)
pO.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pO.line(x="Température (°C)", y="conc_so2", source=source, legend_label="so2",line_width=2, color="yellow", alpha=0.5)
pO.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pO.line(x="Température (°C)", y="conc_pm10", source=source, legend_label="pm10",line_width=2, color="blue", alpha=0.5)
pO.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pO.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm25",line_width=2, color="orange", alpha=0.5)

# legend
pO.legend.location = "top_left"
pO.legend.click_policy="hide"


scriptConcO, divConcO = components(pO)

#pour le mois de novembre
meteo_air_novembre = meteo_air[meteo_air["Month"] == "November"]
meteo_air_novembre = meteo_air_novembre.dropna(axis=0)
meteo_air_novembre = meteo_air_novembre.reset_index()

meteo_air_novembre = meteo_air_novembre.sort_values(by=["Température (°C)"], ascending=False)

source = ColumnDataSource(meteo_air_novembre)
pN = figure(x_axis_label="Température", y_axis_label="Concentration", title="Concentrations par rapport à la température pour le mois de novembre")
pN.circle(x="Température (°C)", y="conc_no2", source=source, size=10, color="red", alpha=0.5)
pN.line(x="Température (°C)", y="conc_no2", source=source, legend_label="no2",line_width=2, color="red", alpha=0.5)
pN.circle(x="Température (°C)", y="conc_o3", source=source, size=10, color="green", alpha=0.5)
pN.line(x="Température (°C)", y="conc_o3", source=source, legend_label="o3",line_width=2, color="green", alpha=0.5)
pN.circle(x="Température (°C)", y="conc_so2", source=source, size=10, color="yellow", alpha=0.5)
pN.line(x="Température (°C)", y="conc_so2", source=source,legend_label="so2", line_width=2, color="yellow", alpha=0.5)
pN.circle(x="Température (°C)", y="conc_pm10", source=source, size=10, color="blue", alpha=0.5)
pN.line(x="Température (°C)", y="conc_pm10", source=source,legend_label="pm10", line_width=2, color="blue", alpha=0.5)
pN.circle(x="Température (°C)", y="conc_pm25", source=source, size=10, color="orange", alpha=0.5)
pN.line(x="Température (°C)", y="conc_pm25", source=source, legend_label="pm20",line_width=2, color="orange", alpha=0.5)

# mettre legende
pN.legend.location = "top_left"
pN.legend.click_policy="hide"


scriptConcN, divConcN = components(pN)

############ graphique moyenne concentrations annuelle
# Calculer la moyenne de chaque colonne
# mean_values = meteo_air.mean()
# # Créer une source de données pour Bokeh
# source = ColumnDataSource(data=dict(x=list(mean_values.index), y=list(mean_values.values)))
# # Créer un graphique en barres
# p = figure(x_range=list(mean_values.index), height=350, title="Moyenne des colonnes")
# p.vbar(x='x', top='y', width=0.9, source=source)
# # Personnaliser le graphique
# p.xgrid.grid_line_color = None
# p.y_range.start = 0

# scriptMoy, divMoy = components(p)

mean_values = meteo_air.mean()
# Create a data source for Bokeh
source = ColumnDataSource(data=dict(x=list(mean_values.index), y=list(mean_values.values)))
# Create a line plot
p = figure(height=350, title="Moyenne des colonnes")
p.line(x='x', y='y', source=source)
# Customize the plot
p.xgrid.grid_line_color = None
p.y_range.start = 0

scriptMoy, divMoy = components(p)

##### graphique ###########
plt.figure(figsize=(23,15))
corr = meteo_air.corr()
sns.heatmap(corr, annot=True)
plt.savefig('static/images/corr.png')

#### mappe ####################
Carte = pd.read_csv('air2022Carte.csv', sep=';')
france_map = folium.Map(location=[46.2276, 2.2137], zoom_start=6.25, min_zoom=5, max_zoom=20)

for index, row in Carte.iterrows():
    # Coordonnées géographiques de la ville
    longitude = row["Longitude"]
    latitude = row["Latitude"]
    
    lib_zone = row["lib_zone"]
    # conc_o3
    conc_o3 = row["conc_o3"]
    conc_no2 = row["conc_no2"]
    conc_pm10 = row["conc_pm10"]
    conc_pm25 = row["conc_pm25"]
    

    # Création du marqueur
    marker = folium.Marker([latitude, longitude], popup=f"{lib_zone} ConcomationO3: {conc_o3} ConcomationNO2: {conc_no2} ConcomationPM10: {conc_pm10}, ConcomationPM25: {conc_pm25} ")
    # Ajout du marqueur à la carte
    marker.add_to(france_map)

france_map.save("./templates/mappe.html") 

######################## Routes ########################################

@app.route('/')
def page():
    return render_template('principalPage.html')

@app.route('/graphiqueMeteo')
def graphiqueMeteo():
    script = server_document('http://localhost:5006/app')
    return render_template('graphiqueMeteo.html',scriptMeteo=scriptMeteo, divMeteo= divMeteo)

@app.route('/graphiqueAir')
def graphiqueAir():
    script = server_document('http://localhost:5006/app')
    return render_template('graphiqueAir.html',script6=script6, div6=div6)

@app.route('/mappe')
def mappe():
    return render_template('mappe.html')

@app.route('/graphique')
def graphique():
    script = server_document('http://localhost:5006/app')
    return render_template('graphique.html',script6=script6,div6=div6,script8=script8, div8=div8,scriptMoy=scriptMoy,divMoy=divMoy,
                           scriptConcJ=scriptConcJ,divConcJ=divConcJ,scritConcF=scritConcFev,divConcF=divConcFev,scriptConcMars=scriptConcMars,divConcMars=divConcMars,
                           scriptConcAvril=scriptConcAvril,divConcAvril=divConcAvril,scriptConcMai=scriptConcMai,divConcMai=divConcMai,scriptConcJuin=scriptConcJuin,
                           divConcJuin=divConcJuin,scriptConcJu=scriptConcJu,divConcJu=divConcJu,scriptConcAo=scriptConcAo,divConcAo=divConcAo,scriptConcS=scriptConcS,divConcS=divConcS,
                            scriptConcO=scriptConcO,divConcO=divConcO,scriptConcN=scriptConcN,divConcN=divConcN,
                            )

if __name__ == '__main__':
    app.run(debug=True)