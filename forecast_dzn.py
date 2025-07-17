import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns={"Price": "Date"})  # Correcting date column name
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[['Date', 'Close']].dropna()
    df = df.set_index('Date').resample('W-MON').last().reset_index()
    return df

btc_df = load_and_prepare_data("Bitcoin.csv")
eth_df = load_and_prepare_data("Ethereum.csv")
gold_df = load_and_prepare_data("Gold.csv")

def linear_regression(X, y):
    X_b = np.c_[np.ones((len(X), 1)), X]
    theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
    return theta

def predict_next(X, theta):
    next_index = np.array([[1, len(X)]])
    return float(next_index @ theta)

def forecast_return(df):
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['Close'].values
    theta = linear_regression(X, y)
    pred_price = predict_next(X, theta)
    last_price = df['Close'].values[-1]
    ret = (pred_price - last_price) / last_price
    return ret, pred_price, last_price

## 🔮 6. Forecast Returns
btc_return, btc_pred, btc_last = forecast_return(btc_df)
eth_return, eth_pred, eth_last = forecast_return(eth_df)
gold_return, gold_pred, gold_last = forecast_return(gold_df)

# Fixed bond return per month (0.55%)
bond_return = 0.0055

# Print returns
print("Bitcoin return:", btc_return)
print("Ethereum return:", eth_return)
print("Gold return:", gold_return)

def write_dzn(filename, gold_ret, crypto_ret, margin_ret, bond_ret):
    content = f"""
    gold_return = {gold_ret:.5f};
    crypto_spot_return = {crypto_ret:.5f};
    crypto_margin_return = {margin_ret:.5f};
    bond_return = {bond_ret:.5f};
    """
    Path(filename).write_text(content.strip())
    print(f"✅ .dzn file saved to: {filename}")

# Example: use BTC for crypto_spot and ETH for margin
write_dzn("week1.dzn", gold_return, btc_return, eth_return, bond_return)