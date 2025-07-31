import numpy as np

def generate_data(n_samples=1000):
    """
    Generates synthetic data for training the anomaly detection model.
    Returns a tuple of (X, y) where X is the feature vector (query length)
    and y is the label (0 for normal, 1 for anomaly).
    """
    # Normal queries
    normal_queries = np.random.normal(loc=100, scale=20, size=int(n_samples * 0.9))

    # Anomalous queries (shorter or longer)
    anomalous_queries = np.concatenate([
        np.random.normal(loc=20, scale=5, size=int(n_samples * 0.05)),
        np.random.normal(loc=500, scale=50, size=int(n_samples * 0.05))
    ])

    X = np.concatenate([normal_queries, anomalous_queries]).reshape(-1, 1)
    y = np.concatenate([np.zeros(len(normal_queries)), np.ones(len(anomalous_queries))])

    return X, y
