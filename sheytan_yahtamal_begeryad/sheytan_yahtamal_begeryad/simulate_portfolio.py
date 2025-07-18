import re
from datetime import datetime
import pandas as pd
from minizinc import Instance, Model, Solver

def recursive_predict(asset, lag_row, w, b, steps):
    lag_list = [lag_row[f"Lag{i+1}"] for i in range(len(w))]
    lag_list = lag_list[::-1]
    for _ in range(steps):
        current_lags = lag_list[-len(w):][::-1]
        pred = sum(w[i] * current_lags[i] for i in range(len(w))) + b
        lag_list.append(pred)
    return pred

def load_decision_dates(dzn_path):
    with open(dzn_path, "r") as f:
        content = f.read()
    match = re.search(r'decision_dates\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not match:
        raise ValueError("Could not find decision_dates in .dzn file")
    return [s.strip().strip('"') for s in match.group(1).split(",")]

def load_weights(file_path):
    text = open(file_path).read()
    w_m = re.search(r"Weights:\s*\[([^\]]+)\]", text)
    b_m = re.search(r"Intercept:\s*([-+]?[0-9]*\.?[0-9]+)", text)
    if not w_m or not b_m:
        raise ValueError(f"Could not parse weights/intercept from {file_path}")
    w = list(map(float, w_m.group(1).split(",")))
    b = float(b_m.group(1))
    return w, b

def load_lag_data(asset):
    df = pd.read_csv(f"./csvs/{asset}_daily_features.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def load_actual_prices(asset):
    df = pd.read_csv(f"./csvs/{asset}_clean.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")

def get_lag_row_before_date(df, date_str):
    date = pd.to_datetime(date_str)
    sub = df[df["Date"] < date]
    if sub.empty:
        raise ValueError(f"No lag features before {date_str}")
    return sub.iloc[-1]

# === Load everything ===

decision_dates = load_decision_dates("all_decision_dates.dzn")

weights = {}
for asset in ["Bitcoin", "Ethereum", "Gold"]:
    w, b = load_weights(f"./regression_out/{asset}_daily_weights.txt")
    weights[asset] = {"w": w, "b": b}

lag_data = {asset: load_lag_data(asset) for asset in ["Bitcoin", "Ethereum", "Gold"]}
actual_prices = {asset: load_actual_prices(asset) for asset in ["Bitcoin", "Ethereum", "Gold"]}

# === Initial state ===

capital    = 50000.0
r_b        = 0.0055
past_bonds = [0.0, 0.0, 0.0, 0.0]
prev_units = [0.0, 0.0, 0.0]   # BTC, ETH, Gold

initial_capital = capital     # for end summary

# Prepare MiniZinc
model  = Model("invest.mzn")
solver = Solver.lookup("cbc")

print("\n=== Starting portfolio simulation ===")
print(f"Initial capital: {initial_capital:.2f}\n")

# === Main loop ===

for i in range(len(decision_dates) - 1):
    today_str = decision_dates[i]
    next_str  = decision_dates[i+1]
    today_dt  = datetime.fromisoformat(today_str)
    next_dt   = datetime.fromisoformat(next_str)
    steps     = (next_dt - today_dt).days

    # 1) Fetch today’s market prices
    price_t = [
        actual_prices["Bitcoin"].loc[today_dt, "Close"],
        actual_prices["Ethereum"].loc[today_dt, "Close"],
        actual_prices["Gold"].loc[today_dt, "Close"],
    ]

    # 2) Forecast next-week prices
    price_pred = []
    for asset in ["Bitcoin", "Ethereum", "Gold"]:
        lag_row = get_lag_row_before_date(lag_data[asset], today_str)
        w, b    = weights[asset]["w"], weights[asset]["b"]
        price_pred.append(recursive_predict(asset, lag_row, w, b, steps))

    # Print market & forecast
    print(f"Week {i+1}: {today_str} -> {next_str}  ({steps} days)")
    print("  Today's prices:     BTC={:.2f}, ETH={:.2f}, GOLD={:.2f}".format(*price_t))
    print("  Forecasted prices:  BTC={:.2f}, ETH={:.2f}, GOLD={:.2f}".format(*price_pred))

    # 3) Solve the MIP
    inst = Instance(solver, model)
    inst["capital"]    = capital
    inst["price_t"]    = price_t
    inst["price_pred"] = price_pred
    inst["prev_h"]     = prev_units
    inst["bonds"]      = past_bonds

    res = inst.solve()

    # 4) Read decisions & compute deltas
    old_units   = prev_units.copy()
    btc_units   = res["x"][0]
    eth_units   = res["x"][1]
    gold_units  = res["x3"]
    g_int       = res["g"]
    b_new       = res["b_new"]

    delta_btc   = btc_units  - old_units[0]
    delta_eth   = eth_units  - old_units[1]
    delta_gold  = gold_units - old_units[2]

    # 5) Actual prices on next decision date
    actual_next = [
        actual_prices["Bitcoin"].loc[next_dt, "Close"],
        actual_prices["Ethereum"].loc[next_dt, "Close"],
        actual_prices["Gold"].loc[next_dt, "Close"],
    ]
    print("  Actual next-date:   BTC={:.2f}, ETH={:.2f}, GOLD={:.2f}".format(*actual_next))

    # 6) Print buy/sell amounts
    print("  Trade decisions:   BTC {:+.4f} units, ETH {:+.4f}, GOLD {:+.4f}, BONDS +{:.2f}".format(
        delta_btc, delta_eth, delta_gold, b_new
    ))

    # 7) Update cash with matured bond
    matured = past_bonds.pop(0) * (1 + r_b)
    capital += matured

    # 8) Subtract net trade cost
    cost = (
        delta_btc  * price_t[0]
      + delta_eth  * price_t[1]
      + delta_gold * price_t[2]
      + b_new
    )
    capital -= cost

    # 9) Roll bond queue & holdings forward
    past_bonds.append(b_new)
    prev_units = [btc_units, eth_units, gold_units]

    # 10) Compute current portfolio value
    portfolio_value = ( capital +
        btc_units  * price_t[0]
      + eth_units  * price_t[1]
      + gold_units * price_t[2]
      + sum(past_bonds[j] * (1 + r_b) for j in range(len(past_bonds)-1))
    )
    print(f"  Portfolio value:   {portfolio_value:.2f}\n")

# === End summary ===

final_value = portfolio_value
total_return = (final_value - initial_capital) / initial_capital * 100

print("=== Simulation complete ===")
print(f"Final portfolio value: {final_value:.2f}")
print(f"Total return:          {total_return:.2f}%\n")
