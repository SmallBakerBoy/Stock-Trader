import market_data as md
import database as db

import pandas as pd
import numpy as np






current_user = 2

def create_portfolio(user):
    SP500 = list(md.get_sp500().values())
    blacklist = db.fetch_blacklist(user)
    companies = [x for x in SP500 if x not in blacklist]

    market_data = md.get_market_data(companies)
    market_data = md.format_market_data(market_data)
    
    components = calc_principal_comps(market_data,4)
    return components

def calc_principal_comps(data,n):
    covariance_matrix = data.cov()
    eigenvalues , eigenvectors = np.linalg.eigh(covariance_matrix)
    return eigenvalues, eigenvectors

market_data = md.get_market_data(['aapl','nvda'])
market_data = md.format_market_data(market_data)

print(calc_principal_comps(market_data,4))

