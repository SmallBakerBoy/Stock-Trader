import pandas as pd
import numpy as np
import sklearn.cluster as sk

import matplotlib.pyplot as plt
import random

market_data = pd.read_csv('data.csv')
market_data = market_data.drop(columns=['Unnamed: 0'])

cluster_amount = 8

def calc_sharpe_ratio(data,company):
    sharpe_ratio = random.randint(1,100)
    return sharpe_ratio

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
    
components = calc_principal_comps(market_data,4)[1:3]


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



clusters = [['AMCR', 'ANET', 'DHI', 'DOW', 'DVA', 'EMR', 'FICO', 'GLW', 'GM', 'GNRC', 'HCA', 'HPQ', 'IDXX', 'IR', 'LHX', 'LOW', 'LVS', 'LYB', 'MSI', 'NDSN', 'NWS', 'OKE', 'ON', 'PNC', 'PNW', 'PSKY', 'SLB', 'TKO', 'VRTX'], ['AAPL', 'ABT', 'ACN', 'ADP', 'AEE', 'AES', 'AFL', 'AKAM', 'AMD', 'AMT', 'AON', 'APP', 'AWK', 'AZO', 'BDX', 'BEN', 'BG', 'BRK-B', 'BSX', 'CAH', 'CBRE', 'CF', 'CFG', 'CHRW', 'CHTR', 'CMI', 'CNP', 'COP', 'CPB', 'DAL', 'DE', 'DRI', 'DTE', 'EME', 'ERIE', 'ESS', 'ETN', 'EXC', 'EXR', 'FANG', 'FCX', 'GD', 'HD', 'HOLX', 'HOOD', 'HST', 'HSY', 'J', 'JCI', 'JNJ', 'KIM', 'KMB', 'LIN', 'LKQ', 'MAR', 'MSCI', 'NEE', 'NFLX', 'NRG', 'OMC', 'PEG', 'PHM', 'PNR', 'PPG', 'PSX', 'RCL', 'RF', 'RMD', 'RTX', 'SNA', 'STZ', 'SW', 'SWK', 'SYK', 'SYY', 'TEL', 'TGT', 'TSLA', 'TTWO', 'UAL', 'UPS', 'USB', 'V', 'VICI', 'VLO', 'VLTO', 'VRSK', 'VST', 'VTRS', 'WAB', 'WAT', 'WDAY', 'WDC', 'WM', 'WMB', 'WRB', 'XEL', 'XOM', 'ZBH'], ['ADSK', 'AEP', 'AJG', 'ALGN', 'APO', 'AVB', 'AXP', 'BAC', 'BK', 'BKNG', 'BKR', 'BLK', 'CAG', 'CDW', 'COIN', 'CTAS', 'CTRA', 'CVX', 'DIS', 'ECL', 'EFX', 'ETR', 'EXE', 'F', 'FITB', 'FRT', 'FSLR', 'FTNT', 'GIS', 'HBAN', 'HIG', 'HSIC', 'HUBB', 'INTC', 'JBL', 'KO', 'LYV', 'MCHP', 'MLM', 'MMM', 'MRK', 'MTD', 'NEM', 'NTAP', 'NVR', 'ORCL', 'OTIS', 'PAYC', 'PAYX', 'PFE', 'PGR', 'PLTR', 'PRU', 'PTC', 'ROP', 'SBUX', 'SRE', 'STE', 'STLD', 'SYF', 'TDG', 'TFC', 'TJX', 'TMUS', 'TPL', 'TRV', 'TTD', 'UHS', 'UNP', 'VRSN', 'WMT', 'WSM', 'XYZ', 'ZBRA'], ['AIG', 'APH', 'ARE', 'BA', 'BF-B', 'CI', 'CINF', 'CLX', 'CNC', 'COST', 'CRL', 'CSCO', 'CTVA', 'CVS', 'DD', 'DECK', 'DLR', 'DOV', 'DPZ', 'DVN', 'EBAY', 'EG', 'EL', 'EOG', 'EPAM', 'EQR', 'EXPD', 'FDS', 'GDDY', 'GE', 'GOOG', 'GPC', 'HLT', 'HPE', 'IEX', 'IFF', 'INCY', 'INVH', 'IP', 'IQV', 'IRM', 'JKHY', 'KLAC', 'LNT', 'MAA', 'MGM', 'MOS', 'NI', 'NOC', 'NVDA', 'NXPI', 'PEP', 'PM', 'POOL', 'PPL', 'PSA', 'ROK', 'RSG', 'SBAC', 'SCHW', 'SJM', 'SPGI', 'TT', 'UNH', 'WBD', 'XYL'], ['ADM', 'BALL', 'BMY', 'BR', 'CMCSA', 'CPAY', 'D', 'DAY', 'DHR', 'DOC', 'DXCM', 'ELV', 'FAST', 'FDX', 'FFIV', 'FISV', 'FOX', 'FOXA', 'GOOGL', 'HAL', 'HII', 'HRL', 'INTU', 'ISRG', 'IT', 'KEY', 'KVUE', 'L', 'LEN', 'LH', 'LULU', 'LW', 'MCK', 'MCO', 'MDT', 'MNST', 'MO', 'MU', 'O', 'PLD', 'QCOM', 'REG', 'RJF', 'SNPS', 'STT', 'T', 'TPR', 'WYNN'], ['ACGL', 'CL', 'COO', 'EQT', 'ES', 'EW', 'FTV', 'GPN', 'GS', 'IBM', 'JBHT', 'LLY', 'MAS', 'MCD', 'META', 'MPWR', 'NDAQ', 'NTRS', 'PCG', 'PFG', 'PG', 'ROL', 'ROST', 'RVTY', 'SWKS', 'ULTA', 'VMC'], ['A', 'ADI', 'ALB', 'AMAT', 'AME', 'AMGN', 'AOS', 'APA', 'APD', 'ARES', 'ATO', 'AVGO', 'AVY', 'AXON', 'BAX', 'BIIB', 'BRO', 'BX', 'C', 'CARR', 'CBOE', 'CCI', 'CEG', 'CHD', 'CMG', 'CMS', 'COF', 'COR', 'CPRT', 'CRM', 'CSGP', 'CTSH', 'DDOG', 'DELL', 'DGX', 'DLTR', 'EA', 'ED', 'EQIX', 'EXPE', 'GEHC', 'GEN', 'GILD', 'GL', 'GWW', 'HON', 'HUM', 'KEYS', 'KKR', 'KMI', 'KR', 'LDOS', 'LMT', 'LRCX', 'LUV', 'MA', 'MDLZ', 'MHK', 'MMC', 'MOH', 'MRNA', 'MS', 'MTB', 'MTCH', 'NCLH', 'NKE', 'NUE', 'NWSA', 'OXY', 'PH', 'PODD', 'PYPL', 'REGN', 'RL', 'SO', 'SPG', 'STX', 'TECH', 'TER', 'TMO', 'TRGP', 'TRMB', 'TXN', 'UBER', 'URI', 'WEC', 'WELL', 'WFC', 'WTW', 'WY', 'YUM', 'ZTS'], ['ABBV', 'ABNB', 'ADBE', 'AIZ', 'ALL', 'ALLE', 'AMP', 'APTV', 'BBY', 'BLDR', 'BXP', 'CAT', 'CB', 'CCL', 'CDNS', 'CME', 'CPT', 'CRWD', 'CSX', 'DASH', 'DG', 'DUK', 'EIX', 'EVRG', 'FE', 'FIS', 'GRMN', 'HAS', 'HWM', 'IBKR', 'ICE', 'ITW', 'IVZ', 'JPM', 'KDP', 'KHC', 'LII', 'MET', 'MKC', 'MPC', 'NOW', 'NSC', 'ODFL', 'ORLY', 'PANW', 'PCAR', 'PKG', 'PWR', 'SHW', 'SMCI', 'TAP', 'TDY', 'TROW', 'TSCO', 'TSN', 'TXT', 'TYL', 'UDR', 'VTR', 'VZ', 'WST']]

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

        for i in range(int(company_amount/len(clusters))):
            results.append(mapping[sharpe_ratios[i]])
    return results


   


components = calc_principal_comps(market_data,4)

clusters = create_clusters(market_data,components,8)

companies = select_companies(market_data,clusters,32)

print(companies)