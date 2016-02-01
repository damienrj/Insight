from flask import Flask, render_template, request, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from sklearn.externals import joblib
import pygal
from pygal.style import LightColorizedStyle

#clf = joblib.load('/home/remote/myproject/model/week2.pkl')

app = Flask(__name__)
app.secret_key='123qasdSFASD2##$#ASFasdFasd@E'

engine = create_engine('postgres://remote@localhost/data')

con = None
con = psycopg2.connect(database = 'data', user = 'remote', host='localhost')

@app.route('/')
def insight():

    return(render_template('insight.html'))

@app.route('/test')
def insight2():

    data = []
    return(render_template('test.html', data = 'Damien'))



@app.route('/app')
def post():
    if request.method == 'POST':
        text = request.form['text']
        restaurant = text.lower()

    else:
        restaurant='129 lake street cafe'

    restaurant = request.args.get('name')
    if restaurant is not None:
        query = "SELECT * FROM recent WHERE businessname = $${}$$".format(restaurant)
        result = pd.read_sql_query(query, engine)
        line_chart = pygal.HorizontalBar(width=350, height=200, style=LightColorizedStyle, explicit_size='true')
        line_chart.title = 'Odds of passing (in %)'
        line_chart.add('Fail', 100*result.fail_odds[0])
        line_chart.add('Pass', 100*result.pass_odds[0])
        chart = line_chart.render(is_unicode=True)
    else:
        chart = ''
        restaurant = ''





    return render_template('app.html', restaurant=restaurant, chart=chart)


@app.route('/old')
def indexPage():
    return(render_template('index.html'))
if __name__ == "__main__":
    app.run(debug = "True")

@app.route('/chart')
def test():
    line_chart = pygal.HorizontalBar(width=400, height=200, style=LightColorizedStyle, explicit_size='true')
    line_chart.title = 'Odss of passing (in %)'
    line_chart.add('Pass', 19.5)
    line_chart.add('Fail', 36.6)

    chart = line_chart.render(is_unicode=True)
    return render_template('app.html', restaurant='test', chart=chart)
