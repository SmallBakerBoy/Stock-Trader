import yfinance as yf
import requests

import pandas as pd
import bs4 as bs
import numpy as np

import datetime

#Format of dictionary is Key = Ticker, Value = object
cached_data = {}

class company():
    def __init__(self,ticker):
        self.ticker = ticker

        self.market_data = []
        self.lastupdate = datetime.datetime.now()

        self.indicators = {}  

    def __str__(self):
        return f'Data for company {self.ticker}:\n{self.market_data}'

    def get_history(self):
        self.market_data = yf.download(self.ticker,auto_adjust=True)['Close']
        self.lastupdate = datetime.datetime.now()

    def update(self):
        pass


def get_sp500():
    sp500_dict = {}

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    content = requests.get(url,headers={'User-Agent':'Stockbot/1.0'}).text
    html = bs.BeautifulSoup(content,'html.parser')
    table = html.find('table',class_='wikitable')
    body = table.find('tbody')
    rows = body.find_all('tr')
    rows.pop(0)
    for i in rows:
        columns = i.find_all('td')
        longname = (columns[1].text).strip()
        ticker = (columns[0].text).strip()
        sp500_dict[longname] = ticker

    for key in sp500_dict:
        sp500_dict[key] = sp500_dict[key].replace('.','-')
    return sp500_dict

def cache_data(data):
    for i in data:
        if i in cached_data:
            cached_data[i].market_data = data[i]
            cached_data[i].lastupdate = datetime.datetime.now()

        else:
            cached_data[i] = company(i)
            cached_data[i].market_data = data[i]
            cached_data[i].lastupdate = datetime.datetime.now()

def check_cache(ticker,period):
    if ticker in cached_data:
        if datetime.datetime.now()-cached_data[ticker].lastupdate > datetime.timedelta(hours=period):
            del cached_data[ticker]
            return False
        return True
    return False

def save_cache(cached_data):
    pass

def load_cache(cached_data):
    pass

def get_market_data(tickers):
    market_data=[]
    tickers.append('^GSPC')
    for i in tickers:
        if check_cache(i,1) == True:
           market_data.append([i,cached_data[i].market_data]) 
           tickers.remove(i)
    market_data = yf.download(tickers,auto_adjust=True,period='3y')['Close']
    cache_data(market_data)
    return market_data

def format_market_data(market_data):
    close_prices = pd.DataFrame({ticker: market_data[ticker].values for ticker in market_data})
    
    sufficient_data = close_prices.columns[close_prices.count() > 0.7*len(close_prices)]
    close_prices = close_prices[sufficient_data]

    daily_returns = close_prices.pct_change()
    return daily_returns.dropna()

