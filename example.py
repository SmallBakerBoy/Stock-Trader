import pandas as pd
import html5lib
import ssl
import numpy as np
import yfinance as yf
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import StringIO


    


# 1. Market correlation features
market_returns = returns.mean(axis=1)  # Use average as market proxy
market_corr_features = []
for ticker in returns.columns:
    ticker_returns = returns[ticker].dropna()
    if len(ticker_returns) > 60:
        # Calculate correlation with market
        common_dates = ticker_returns.index.intersection(market_returns.index)
        if len(common_dates) > 60:
            corr = np.corrcoef(ticker_returns[common_dates], market_returns[common_dates])[0, 1]
            market_corr_features.append(corr if not np.isnan(corr) else 0.5)
        else:
            market_corr_features.append(0.5)  # Default correlation
    else:
        market_corr_features.append(0.5)  # Default correlation

# 2. Volatility (standard deviation of returns)
volatilities = returns.std().values
volatilities = np.nan_to_num(volatilities, nan=np.nanmean(volatilities))

# 3. Beta calculation (more robust)
betas = []
for ticker in returns.columns:
    ticker_returns = returns[ticker].dropna()
    if len(ticker_returns) > 60:
        common_dates = ticker_returns.index.intersection(market_returns.index)
        if len(common_dates) > 60:
            # Calculate beta using covariance
            cov = np.cov(ticker_returns[common_dates], market_returns[common_dates])[0, 1]
            var = np.var(market_returns[common_dates])
            beta = cov / var if var != 0 and not np.isnan(cov) else 1.0
            betas.append(beta)
        else:
            betas.append(1.0)
    else:
        betas.append(1.0)

# 4. Correlation-based features
corr_matrix = returns.corr()
corr_matrix = corr_matrix.fillna(0.5)  # Fill NaN with neutral correlation
np.fill_diagonal(corr_matrix.values, 1)

# Average correlation with other stocks
avg_correlations = corr_matrix.mean(axis=1).values
avg_correlations = np.nan_to_num(avg_correlations, nan=0.5)

# Standard deviation of correlations (diversification measure)
std_correlations = corr_matrix.std(axis=1).values
std_correlations = np.nan_to_num(std_correlations, nan=0.2)

# Create enhanced feature matrix
enhanced_features = np.column_stack([
    market_corr_features,  # Correlation with market
    volatilities,          # Volatility
    betas,                # Beta
    avg_correlations,     # Average correlation with all stocks
    std_correlations      # Std of correlations (diversification measure)
])

# Check for any remaining NaN values and replace them
enhanced_features = np.nan_to_num(enhanced_features, nan=0.5)

# Normalize features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
enhanced_features = scaler.fit_transform(enhanced_features)

# Use enhanced features directly for clustering instead of distance matrix
distance_matrix = enhanced_features

# Update tickers list to match the filtered data
tickers = valid_tickers.tolist()
print(f"Created enhanced feature matrix with {enhanced_features.shape[1]} features for clustering")

# -----------------------------
# 3. Dimensionality reduction with PCA
# -----------------------------
# Use 4 principal components for clustering
pca = PCA(n_components=min(distance_matrix.shape))
pca_features = pca.fit_transform(distance_matrix)

# -----------------------------
# 4. Clustering Mode Selection
# -----------------------------

def optimal_clustering_mode(pca_features):
    """Determine optimal number of clusters using silhouette score"""
    num_samples = len(pca_features)
    if num_samples < 3:
        print(f"Warning: Only {num_samples} samples available. Need at least 3 for clustering analysis.")
        return 1, np.zeros(num_samples, dtype=int)
    
    max_k = min(50, num_samples - 1)
    range_k = range(2, max_k + 1)
    sil_scores = []
    
    for k in range_k:
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(pca_features)
        score = silhouette_score(pca_features, labels)
        sil_scores.append(score)
    
    optimal_k = range_k[np.argmax(sil_scores)]
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    labels = kmeans.fit_predict(pca_features)
    print(f"Optimal clustering: {optimal_k} clusters (silhouette score: {max(sil_scores):.3f})")
    return optimal_k, labels

def user_defined_clustering_mode(pca_features):
    """Allow user to specify the number of clusters with balanced distribution"""
    num_samples = len(pca_features)
    max_reasonable = min(num_samples // 10, 25)  # Ensure at least 10 companies per cluster on average
    
    print(f"Note: With {num_samples} companies, recommending 2-{max_reasonable} clusters for meaningful sizes")
    
    while True:
        try:
            user_k = int(input(f"Enter number of clusters (2-{max_reasonable}): "))
            if 2 <= user_k <= max_reasonable:
                break
            else:
                print(f"Please enter a number between 2 and {max_reasonable}")
        except ValueError:
            print("Please enter a valid integer")
    
    # Use multiple runs and select best result to avoid tiny clusters
    best_labels = None
    best_score = -1
    best_balance = float('inf')
    
    for run in range(10):  # Try multiple random initializations
        kmeans = KMeans(n_clusters=user_k, random_state=42+run, n_init=20)
        labels = kmeans.fit_predict(pca_features)
        
        # Calculate cluster balance (prefer more evenly sized clusters)
        cluster_sizes = [np.sum(labels == i) for i in range(user_k)]
        min_size = min(cluster_sizes)
        max_size = max(cluster_sizes)
        balance_ratio = max_size / min_size if min_size > 0 else float('inf')
        
        # Calculate silhouette score for quality
        if len(set(labels)) > 1:
            sil_score = silhouette_score(pca_features, labels)
        else:
            sil_score = -1
        
        # Prefer solutions with better balance and reasonable silhouette score
        if min_size >= 5 and (balance_ratio < best_balance or (balance_ratio == best_balance and sil_score > best_score)):
            best_labels = labels.copy()
            best_score = sil_score
            best_balance = balance_ratio
    
    if best_labels is not None:
        labels = best_labels
        cluster_sizes = [np.sum(labels == i) for i in range(user_k)]
        print(f"User-defined clustering: {user_k} clusters")
        print(f"Cluster sizes: {cluster_sizes} (balance ratio: {best_balance:.2f})")
    else:
        # Fallback to simple kmeans if no good solution found
        kmeans = KMeans(n_clusters=user_k, random_state=42, n_init=20)
        labels = kmeans.fit_predict(pca_features)
        print(f"User-defined clustering: {user_k} clusters (using fallback method)")
    
    return user_k, labels

def minimum_size_clustering_mode(pca_features, min_cluster_size=20):
    """Clustering with minimum cluster size constraint"""
    num_samples = len(pca_features)
    
    if num_samples < min_cluster_size:
        print(f"Warning: Not enough companies ({num_samples}) to create clusters with minimum size {min_cluster_size}")
        return 1, np.zeros(num_samples, dtype=int)
    
    # Start with more clusters and merge small ones
    initial_k = min(25, num_samples // min_cluster_size + 3)
    kmeans = KMeans(n_clusters=initial_k, random_state=42)
    labels = kmeans.fit_predict(pca_features)
    
    # Merge small clusters function
    def merge_small_clusters(labels, min_size, features):
        unique_labels = np.unique(labels)
        cluster_sizes = [np.sum(labels == label) for label in unique_labels]
        
        while min(cluster_sizes) < min_size and len(unique_labels) > 1:
            # Find the smallest cluster
            smallest_cluster_idx = np.argmin(cluster_sizes)
            smallest_cluster_label = unique_labels[smallest_cluster_idx]
            
            # Find the closest cluster to merge with
            smallest_cluster_points = features[labels == smallest_cluster_label]
            smallest_cluster_center = np.mean(smallest_cluster_points, axis=0)
            
            min_distance = float('inf')
            merge_target = None
            
            for other_label in unique_labels:
                if other_label != smallest_cluster_label:
                    other_cluster_points = features[labels == other_label]
                    other_cluster_center = np.mean(other_cluster_points, axis=0)
                    distance = np.linalg.norm(smallest_cluster_center - other_cluster_center)
                    
                    if distance < min_distance:
                        min_distance = distance
                        merge_target = other_label
            
            # Merge the smallest cluster with its closest neighbor
            labels[labels == smallest_cluster_label] = merge_target
            
            # Update unique labels and cluster sizes
            unique_labels = np.unique(labels)
            cluster_sizes = [np.sum(labels == label) for label in unique_labels]
        
        # Relabel clusters to be consecutive starting from 0
        new_labels = np.zeros_like(labels)
        for i, old_label in enumerate(unique_labels):
            new_labels[labels == old_label] = i
        
        return new_labels, len(unique_labels)
    
    labels, final_k = merge_small_clusters(labels, min_cluster_size, pca_features)
    print(f"Minimum size clustering: {final_k} clusters (minimum {min_cluster_size} companies each)")
    return final_k, labels

while True:
    try:
        mode = int(input("Enter mode (1-3): "))
        if mode in [1, 2, 3]:
            break
        else:
            print("Please enter 1, 2, or 3")
    except ValueError:
        print("Please enter a valid integer")

# Apply selected clustering mode
num_samples = len(pca_features)
if mode == 1:
    optimal_k, labels = optimal_clustering_mode(pca_features)
elif mode == 2:
    optimal_k, labels = user_defined_clustering_mode(pca_features)
else:  # mode == 3
    optimal_k, labels = minimum_size_clustering_mode(pca_features)

