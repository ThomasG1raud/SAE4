# importing flask
from flask import Flask, render_template
  
# importing pandas module
import pandas as pd
  
  
app = Flask(__name__)
  
# route to html page - "table"
@app.route('/')
def page():
    return render_template('principalPage.html')
    


@app.route('/table')
def table():
    # converting csv to html
    data = pd.read_csv('donneMeteo.csv',sep=';')
    data1=data.head()
    return render_template('table.html', tables=[data1.to_html()], titles=[''])




if __name__ == '__main__':
    app.run(debug=True)
    