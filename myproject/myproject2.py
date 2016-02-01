from flask import Flask, render_template, request, url_for, flash
import pandas as pd
import Quandl
from seaborn import color_palette

# imports for Bokeh plotting
from bokeh.plotting import figure
from bokeh.embed import file_html, components

def stock_price(stock_name):

    mydata = Quandl.get("WIKI/" + stock_name,
      trim_start="2000-01-01", authtoken = 'zs3CZKMZ8zBpajjMPLws')
    return(mydata)

app = Flask(__name__)
app.secret_key='123qasdSFASD2##$#ASFasdFasd@E'

@app.route('/about')
def aboutpage():

    return(render_template('about.html'))

@app.route('/')
def indexPage():
    # generate some random integers, sorted
    # create a new plot with a datetime axis type
    stock = 'GOOG'
    mydata = stock_price(stock)
    p = figure(title = 'End of Day Stock Prices (2000+)'
        , width=600, height=400, x_axis_type="datetime",
        toolbar_location="below",  x_axis_label = 'Date', y_axis_label = '$')

    p.line(mydata.index, mydata['Close'], color='navy', alpha=1, legend = stock
        ,line_width = 1.5)
    # create the HTML elements to pass to template
    p.legend.orientation = "top_left"
    figJS,figDiv = components(p)
    return(render_template('figures.html', script=figJS, div=figDiv))

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    stocks = text.upper()
    stocks = [x.strip().upper() for x in stocks.split(',')]
    colors = color_palette("husl", len(stocks)).as_hex()
    p = figure(title = 'End of Day Stock Prices (2000+)'
        , width=600, height=400, x_axis_type="datetime",
        toolbar_location="below", x_axis_label = 'Date', y_axis_label = '$')


    i = 0

    for stock in stocks:
        try:
            mydata = stock_price(stock)
            p.line(mydata.index, mydata['Close'],
                color=colors[i], alpha=1, legend = stock, line_width = 1.5)
            i+=1
        except:
            flash(stock + ' not found!')
    # create the HTML elements to pass to template
    p.legend.orientation = "top_left"
    figJS,figDiv = components(p)
    return(render_template('figures.html', script=figJS, div=figDiv))

if __name__ == "__main__":
    app.run(debug = "False", port=33507)
