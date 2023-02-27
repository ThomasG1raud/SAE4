# importing flask
from flask import Flask, render_template
  
# importing pandas module
import pandas as pd
  
  
app = Flask(__name__)
  
# route to html page - "table"
@app.route('/')
def page():
    return render_template('principalPage.html')
    


@app.route('/tableMeteo')
def tableMeteo():
    # converting csv to html
    meteo = pd.read_csv('donneMeteo.csv',sep=';')
    meteo1=meteo.head()
    return render_template('tableMeteo.html', tables=[meteo1.to_html()], titles=[''])


@app.route('/tableAir')
def tableAir():
    # converting csv to html
    air = pd.read_csv('openaq.csv',sep=';')
    air1=air.head()
    return render_template('tableAir.html', tables=[air1.to_html()], titles=[''])




if __name__ == '__main__':
    app.run(debug=True)
    