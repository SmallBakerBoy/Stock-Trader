from .market_data import get_sp500,get_market_data,format_market_data
from .database import get_user_risk,fetch_blacklist,save_trades

import pandas as pd
import numpy as np
import yfinance as yf

import sklearn.cluster as sk
import cvxpy as cp

#Calculates the beta of a single company
def calc_beta(data,company):
    market_variance = data['^GSPC'].var()

    #Calculates the returns covariance of a stock against the market over the data period
    daily_average_company_returns = (sum(data[company]) / len(data[company]))
    daily_average_market_returns = (sum(data['^GSPC']) / len(data['^GSPC']))

    individual_covariance = 0
    for i in range(len(data[company])):
        individual_covariance += (((data[company])[i+1]) - (daily_average_company_returns)) * (((data['^GSPC'])[i+1]) - (daily_average_market_returns))
    individual_covariance /= (len(data[company]) - 1)
    beta = individual_covariance / market_variance
    return beta

def calc_expected_returns(data,company):
    t_bonds= yf.Ticker('^TNX').history()['Close']
    risk_free_rate = float(t_bonds.iloc[-1]) / 100

    expected_market_growth = 0.12
    beta = calc_beta(data,company)
    market_risk_premium = expected_market_growth - risk_free_rate

    expected_returns = risk_free_rate + beta * market_risk_premium
    return expected_returns,risk_free_rate

#Calculates the sharpe ratio of a single company
def calc_sharpe_ratio(data,company):
    beta = calc_beta(data,company)
    expected_returns,risk_free_rate = calc_expected_returns(data,company)

    sharpe_ratio = (expected_returns-risk_free_rate) / beta
    return sharpe_ratio

# Calculates the top n principal components from a list of returns for many companies
def calc_principal_comps(data,n):
    covariance_matrix = data.cov()
    eigenvalues , eigenvectors = np.linalg.eigh(covariance_matrix)
    
    #Maps eigenvectors to corresponding eigenvalue
    mapping = {}
    for i in range(len(eigenvalues)):
        mapping[eigenvalues[i]]= eigenvectors[i]

    #Sorts eigenvectors into descending order
    list(eigenvalues).sort(reverse = True) 

    #Returns the top n eigenvectors and replaces them with eigenvalues
    results = []
    for i in range(n):
        results.append(mapping[eigenvalues[i]]) 

    return results 

def create_clusters(data,components,cluster_amount):
    components = np.array(components).transpose()
    #Creates cluster model then fits our data to that model
    kmeans_clustering = sk.KMeans(random_state=42, n_clusters=cluster_amount).fit(components) 

    #Matches the cluster number to the correct company
    company_clusters = {}
    for i in range(len(kmeans_clustering.labels_)):
        company_clusters[list(data.columns)[i]] = int(kmeans_clustering.labels_[i])

    #Creates 2D array with same amount of lists as clusters
    clusters = []
    for i in range(cluster_amount):
        clusters.append([])
    #sorts company into lists based off their clusters
    for i in company_clusters:
        clusters[company_clusters[i]].append(i)

    return clusters #returns list of clusters of companies

def select_companies(data,clusters,company_amount):
    results = []
    for cluster in clusters:
        sharpe_ratios = []
        for i in cluster:
            sharpe_ratios.append(calc_sharpe_ratio(data,i))
        
        mapping = {}
        for i in range(len(sharpe_ratios)):
            mapping[sharpe_ratios[i]]= cluster[i]
        list(sharpe_ratios).sort(reverse = True)

        for i in range(int(company_amount//len(clusters))):
            results.append(mapping[sharpe_ratios[i]])
    return results

def weight_conversion(data,weights,budget):
    investments = []
    for stock in weights:
        value = stock[1] * budget
        stock_price = (data[stock[0]]).values[-1]
        stock[1] = round(value / stock_price,2)
        investments.append(stock)
    return investments

def queue(settings):
    print((settings))
    return 'OK',200

def create_portfolio(user):
    SP500 = list(get_sp500().values())
    blacklist = fetch_blacklist(user)
    companies = [x for x in SP500 if x not in blacklist]

    market_data_raw = get_market_data(companies)
    market_data_pct = format_market_data(market_data_raw)

    components = calc_principal_comps(market_data_pct,4)

    clusters = create_clusters(market_data_pct,components,8)
    companies = select_companies(market_data_pct,clusters,25)

    
    return companies
    #Converts risk from percentage to a value between 0 and 2 for beta
    risk_max = get_user_risk() / 50


    s = cp.Variable()
    b = cp.Variable()
    

    objective = cp.Maximize(s)
    constraints = [b <= risk_max]


    def update_portfolio(user):
        pass

'''companies = list(get_sp500().values())
market_data_raw = get_market_data(companies)
market_data_pct = format_market_data(market_data_raw)

weights = [['AAPL',0.12],['NVDA',0.32],['AMZN',0.36],['PLTR',0.2]]
trades = weight_conversion(market_data_raw,weights,10000)
print(save_trades(2,trades))'''
