import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def detect_anomalies(df: pd.DataFrame, target_column: str) -> dict:
    """
    Uses Isolation Forest to detect anomalies in a numeric column.
    """
    if target_column not in df.columns or not np.issubdtype(df[target_column].dtype, np.number):
        return {"error": f"Column {target_column} must be numeric for anomaly detection"}

    model = IsolationForest(contamination=0.05, random_state=42)
    # Fit model on the single column reshaping it to 2D
    X = df[[target_column]].dropna()
    if len(X) == 0:
        return {"error": "Insufficient data"}
        
    preds = model.fit_predict(X)
    
    # -1 for anomalies, 1 for normal
    anomalies = X[preds == -1]
    
    result = {
        "total_anomalies": int(len(anomalies)),
        "anomaly_indices": anomalies.index.tolist(),
        "anomaly_values": anomalies[target_column].tolist()
    }
    return result

def detect_anomalies_dbscan(df: pd.DataFrame, columns: list) -> dict:
    """
    Uses DBSCAN to cluster and find multidimensional anomalies.
    """
    sub_df = df[columns].dropna()
    if len(sub_df) == 0:
         return {"error": "Insufficient data for DBSCAN"}
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(sub_df)
    
    db = DBSCAN(eps=3.0, min_samples=2).fit(scaled_data)
    # -1 identifies noisy samples (anomalies)
    outliers = sub_df[db.labels_ == -1]
    
    return {
        "dbscan_anomalies": len(outliers),
        "outlier_indices": outliers.index.tolist()
    }

def calculate_trend(df: pd.DataFrame, target_column: str, window: int = 7) -> dict:
    """
    Calculates a simple moving average to identify trends.
    """
    if target_column not in df.columns or not np.issubdtype(df[target_column].dtype, np.number):
        return {"error": f"Column {target_column} must be numeric for trend analysis"}
        
    # Moving Average
    ma = df[target_column].rolling(window=window, min_periods=1).mean()
    
    return {
        "moving_average": ma.replace({np.nan: None}).tolist()
    }
    
def forecast_neural_network(df: pd.DataFrame, target_column: str, periods: int = 5) -> dict:
    """
    Mocks a Deep Learning Time-Series forecasting model (LSTM/TensorFlow type)
    to predict future outcomes.
    """
    # Simple extrapolation mock for UI presentation
    last_val = df[target_column].dropna().iloc[-1]
    forecast = []
    
    # Generate some slightly random upward trajectory for the mock prediction
    current = last_val
    for _ in range(periods):
        current = current * np.random.uniform(1.0, 1.05)
        forecast.append(current)
        
    return {
        "forecasted_periods": periods,
        "predictions": forecast
    }
