# importing flask
from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
  
  
app = Flask(__name__)
  
meteo = pd.read_csv('donneMeteo.csv',sep=';', index_col='Date', parse_dates=True)
air = pd.read_csv('openaq.csv', sep=';', index_col='Last Updated', parse_dates=True)
meteoAir = pd.concat([meteo, air])
#meteoAir.reset_index(inplace=True, drop=True)



# route to html page - "table"
@app.route('/')
def page():
    return render_template('principalPage.html')
    


@app.route('/tableMeteo')
def tableMeteo():
    # converting csv to html
    return render_template('tableMeteo.html', tables=[meteo.head().to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    # converting csv to html
    return render_template('tableAir.html', tables=[air.head().to_html()], titles=[''])


@app.route('/tableMeteoAir')
def tableMeteoAir():
    # converting csv to html
    return render_template('tableMeteoAir.html', tables=[meteoAir.head().to_html()], titles=[''])
   




if __name__ == '__main__':
    app.run(debug=True)
    