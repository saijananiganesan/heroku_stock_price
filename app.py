import numpy as np 
from flask import Flask, request, render_template, abort, Response,url_for
from bokeh.plotting import figure
from bokeh.embed import components
import requests 
import pandas as pd 
from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d
from bokeh.io import output_file, show, curdoc, export_png, export_svgs
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import row,column


def get_stock_data(stock='ADAP'):
	url='https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+stock+'&interval=5min&apikey=QY9UJA149OLAIWCW'
	response=requests.get(url);
	if response.status_code!=200:
		print ("Error....unable to fetch data from AlphaAdvantage, please try another entry")
	data_dic=response.json();
	try:
		time_series=data_dic['Weekly Time Series']
		train = pd.DataFrame.from_dict(time_series, orient='index')
		train.reset_index(level=0, inplace=True)
		train.rename(columns={'index':'Date','1. open':'Open',
					 '2. high':'High', '3. low':'Low','4. close':'Close',
					  '5. volume':'Volume'},inplace=True)
		train['Date']= pd.to_datetime(train['Date'])
	except:
		train='None'

	return train


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/form/', methods=['GET', 'POST'])
def form():
	if request.method == 'POST':
		Ticker=request.form['Ticker']
		print ("Ticker",Ticker)
		stock_data=get_stock_data(Ticker)

		if stock_data.__class__.__name__ == 'DataFrame':
			tabs_S=[]
			plot = figure(plot_width=1000, plot_height=500, toolbar_location="below",x_axis_type="datetime",
					title='Price of Requested Stock [Opened Prices]')
			plot.line(stock_data['Date'],stock_data['Open'], color='gray',line_width=1)
			plot.circle(stock_data['Date'],stock_data['Open'],color='blue',fill_alpha=0.3,size=5)
			plot.title.text_font_size='12pt'
			plot.title.align="center"
			plot.title.vertical_align='top'
			plot.xaxis.major_label_text_font_size="14pt"
			plot.yaxis.major_label_text_font_size="14pt"
			plot.xaxis.axis_label = "Date"
			plot.xaxis.axis_label_text_font_size='14pt'
			plot.yaxis.axis_label = 'Price($)'
			plot.yaxis.axis_label_text_font_size='14pt'
			stock_data['Open']=stock_data['Open'].astype(float)
			plot.y_range=Range1d(stock_data['Open'].min(), stock_data['Open'].max())

			tabs_S.append(Panel(child=row(plot), title='Price: Open'))

			plotH = figure(plot_width=1000, plot_height=500, toolbar_location="below",x_axis_type="datetime",
							title='Price of Requested Stock [High Prices]')

			plotH.line(stock_data['Date'],stock_data['High'], color='gray',line_width=1)
			plotH.circle(stock_data['Date'],stock_data['High'],color='blue',fill_alpha=0.3,size=5)
			plotH.title.text_font_size='12pt'
			plotH.title.align="center"
			plotH.title.vertical_align='top'
			plotH.xaxis.major_label_text_font_size="14pt"
			plotH.yaxis.major_label_text_font_size="14pt"
			plotH.xaxis.axis_label = "Date"
			plotH.xaxis.axis_label_text_font_size='14pt'
			plotH.yaxis.axis_label = 'Price($)'
			plotH.yaxis.axis_label_text_font_size='14pt'
			stock_data['High']=stock_data['High'].astype(float)
			plotH.y_range=Range1d(stock_data['High'].min(), stock_data['High'].max())

			tabs_S.append(Panel(child=row(plotH), title='Price: high'))

			plotL = figure(plot_width=1000, plot_height=500, toolbar_location="below",x_axis_type="datetime",
							title='Price of Requested Stock [Low Prices]')

			plotL.line(stock_data['Date'],stock_data['Low'], color='gray',line_width=1)
			plotL.circle(stock_data['Date'],stock_data['Low'],color='blue',fill_alpha=0.3,size=5)
			plotL.title.text_font_size='12pt'
			plotL.title.align="center"
			plotL.title.vertical_align='top'
			plotL.xaxis.major_label_text_font_size="14pt"
			plotL.yaxis.major_label_text_font_size="14pt"
			plotL.xaxis.axis_label = "Date"
			plotL.xaxis.axis_label_text_font_size='14pt'
			plotL.yaxis.axis_label = 'Price($)'
			plotL.yaxis.axis_label_text_font_size='14pt'
			stock_data['Low']=stock_data['Low'].astype(float)
			plotL.y_range=Range1d(stock_data['Low'].min(), stock_data['Low'].max())

			tabs_S.append(Panel(child=row(plotL), title='Price: low'))


			plotC = figure(plot_width=1000, plot_height=500, toolbar_location="below",x_axis_type="datetime",
							title='Price of Requested Stock [Closed Prices]')

			plotC.line(stock_data['Date'],stock_data['Close'], color='gray',line_width=1)
			plotC.circle(stock_data['Date'],stock_data['Close'],color='blue',fill_alpha=0.3,size=5)
			plotC.title.text_font_size='12pt'
			plotC.title.align="center"
			plotC.title.vertical_align='top'
			plotC.xaxis.major_label_text_font_size="14pt"
			plotC.yaxis.major_label_text_font_size="14pt"
			plotC.xaxis.axis_label = "Date"
			plotC.xaxis.axis_label_text_font_size='14pt'
			plotC.yaxis.axis_label = 'Price($)'
			plotC.yaxis.axis_label_text_font_size='14pt'
			stock_data['Close']=stock_data['Close'].astype(float)
			plotC.y_range=Range1d(stock_data['Close'].min(), stock_data['Close'].max())

			tabs_S.append(Panel(child=row(plotC), title='Price: closed'))


			tabs = Tabs(tabs=tabs_S)
			curdoc().add_root(tabs)

			script, div = components(tabs)
			kwargs = {'script': script, 'div': div}
			kwargs['title'] = 'bokeh-with-flask'    
			return render_template('output.html', **kwargs)   
		else:
			return "<h1>You entered the wrong ticker, try again!.</h1>"


	return render_template('form.html')


if __name__ == '__main__':
	app.run(debug=True)

