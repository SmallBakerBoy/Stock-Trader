import market_data as md
import database as db

import pandas as pd
import numpy as np

import sklearn.cluster as sk
import cvxpy as cp

# Calculates the top n principal components from a list of returns for many companies
def calc_principal_comps(data,n):
    covariance_matrix = data.cov()
    eigenvalues , eigenvectors = np.linalg.eigh(covariance_matrix)
    
    mapping = {}
    for i in range(len(eigenvalues)):
        mapping[eigenvalues[i]]= eigenvectors[i]
    list(eigenvalues).sort(reverse = True)

    results = []
    for i in range(n):
        results.append(mapping[eigenvalues[i]])

    return results 

def create_clusters(data,components,cluster_amount):
    components = np.array(components).transpose()
    kmeans_clustering = sk.KMeans(random_state=42, n_clusters=cluster_amount).fit(components)

    company_clusters = {}
    for i in range(len(kmeans_clustering.labels_)):
        company_clusters[list(data.columns)[i]] = int(kmeans_clustering.labels_[i])

    clusters = []
    for i in range(cluster_amount):
        clusters.append([])

    for i in company_clusters:
        clusters[company_clusters[i]].append(i)

    return clusters

#Calculates the sharpe ratio of a single company
def calc_sharpe_ratio(data,company):
    sharpe_ratio = 0
    return sharpe_ratio

#Calculates the beta of a single company
def calc_beta(data):
    pass

def create_portfolio(user):
    SP500 = list(md.get_sp500().values())
    blacklist = db.fetch_blacklist(user)
    companies = [x for x in SP500 if x not in blacklist]

    market_data = md.get_market_data(companies)
    market_data = md.format_market_data(market_data)

    components = calc_principal_comps(market_data,4)

    clusters = create_clusters(market_data,components,8)
    

    
    
print(create_portfolio(2))



