# process_data.py
import pandas as pd
import os

def load_real_time_data(file_path="realtime_data.csv", smooth=False, window=10):
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=["timestamp", "value"])
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna().sort_values(by="timestamp")
    if smooth:
        df['smoothed'] = df['value'].rolling(window=window).mean()
    return df

def load_gold_data(file_path="kaggle_gold.csv", smooth=False, window=10):
    df = pd.read_csv(file_path, sep=';')  # Add sep=';' here!
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Price'] = pd.to_numeric(df['Close'], errors='coerce')  # Use 'Close' for price
    df = df.dropna()
    if smooth:
        df['smoothed'] = df['Price'].rolling(window=window).mean()
    return df
