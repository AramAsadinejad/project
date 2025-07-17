import pandas as pd
import numpy as np
from minizinc import Instance, Model, Solver

# -------- MiniZinc Setup --------
gecode = Solver.lookup("gecode")
model = Model("investment_model_with_bond_lock.mzn")

# -------- Load Data --------
def load_asset(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[['Date', 'Close']].dropna()
    df = df.set_index('Date').resample('W-MON').last().reset_index()
    return df

btc = load_asset("Bitcoin.csv")
eth = load_asset("Ethereum.csv")
gold = load_asset("Gold.csv")

# -------- Forecast Function --------
def forecast(df):
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["Close"].values
    X_b = np.c_[np.ones((len(X), 1)), X]
    theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
    next_val = np.array([[1, len(X)]]) @ theta
    return float((next_val - y[-1]) / y[-1])

# -------- Simulation Loop --------
bond_history = [0, 0, 0, 0]  # 4 هفته قفل سرمایه اوراق

for week in range(1, 11):
    gold_ret = forecast(gold)
    btc_ret = forecast(btc)
    eth_ret = forecast(eth)
    bond_ret = 0.0055
    max_bond_invest = max(0.0, 1.0 - sum(bond_history))

    instance = Instance(gecode, model)
    instance["gold_return"] = gold_ret
    instance["crypto_spot_return"] = btc_ret
    instance["crypto_margin_return"] = eth_ret
    instance["bond_return"] = bond_ret
    instance["max_bond_investment"] = max_bond_invest

    result = instance.solve()
    print(f"\n📅 Week {week}")
    print(f"Gold: {result['gold_percent']}%")
    print(f"Crypto Spot (BTC): {result['crypto_spot_fraction']:.2f}")
    print(f"Crypto Margin (ETH): {result['crypto_margin_fraction']:.2f} x{result['leverage']}")
    print(f"Bonds: {result['bond_fraction']:.2f}")

    # Update bond lock tracker
    bond_history = bond_history[1:] + [result['bond_fraction']]
