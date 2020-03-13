import datetime as dt 
import matplotlib.pyplot as plt 
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
style.use('fivethirtyeight')
font = {'family': 'monospace','color': 'dodgerblue','weight': 'black','size': 20,}
start = dt.datetime(2015,1,1)
end = dt.datetime.now()

def Get_Data():
    stockdf = web.DataReader ("NKE",'yahoo',start,end) 
    stockdf.to_excel('STOCK.xls') 

def Graph():
    df = pd.read_excel('STOCK.xls',parse_dates = True, index_col = 0)

    df['Adj Close'].plot() 

    df['100 Moving Average'] = df['Adj Close'].rolling(window=100, min_periods = 0).mean()
    print (df.tail())

    ax1 = plt.subplot2grid((6,1),(0,0), rowspan=4, colspan=2)
    ax2 = plt.subplot2grid((6,1),(5,0), rowspan=2, colspan=2, sharex=ax1)

    ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['100 Moving Average'])
    ax2.bar(df.index, df['Volume'])

    ax1.set_title('Nike Stock Price & 100 Moving Average',fontdict=font)
    ax1.set_ylabel('Price')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Volume')
    ax1.legend(('Adj Close', '100 Moving Average'), loc='upper left', shadow=True)

    plt.show()

def Candlestick():
    df = pd.read_excel('STOCK.xls',parse_dates = True, index_col = 0)

    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample ('10D').sum()

    df_ohlc.reset_index(inplace=True)

    df_ohlc['Date']= df_ohlc['Date'].map(mdates.date2num)

    ax1 = plt.subplot2grid((6,1),(0,0), rowspan=4, colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=4, colorup='g')

    ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values) 

    ax1.set_title('Nike 10 Day Stock Price & Volume',fontdict=font)
    ax1.set_ylabel('Price')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Volume')

    plt.show()
