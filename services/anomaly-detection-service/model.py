import numpy as np
from sklearn.ensemble import IsolationForest
from data_generator import generate_data

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)

    def train(self):
        """
        Generates data and trains the Isolation Forest model.
        """
        X, _ = generate_data()
        self.model.fit(X)

    def predict(self, X):
        """
        Predicts if the given data point is an anomaly.
        Returns -1 for anomalies, 1 for normal data.
        """
        return self.model.predict(X)[0] == -1
