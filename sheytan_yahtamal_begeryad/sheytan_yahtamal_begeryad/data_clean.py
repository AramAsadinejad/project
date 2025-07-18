import pandas as pd

#Configuration parameters
DAILY_LAGS = 7
WEEKLY_LAGS = 4
LAMBDA = 1.0
START_DATE = pd.Timestamp("2024-04-01")
LAG_START_DATE = pd.Timestamp("2024-03-25")

def load_and_clean(file_path, asset_name):
    df = pd.read_csv(file_path)
    df = df.rename(columns={df.columns[0]: 'Date', 'Close': 'Close'})
    df = df[['Date', 'Close']]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    daily = df.resample('D').asfreq()
    daily['Close'] = daily['Close'].ffill()
    weekly = daily.resample('W-FRI').last()
    return daily, weekly

def prepare_features(df, look_back, freq_type):
    df = df.copy()
    for i in range(1, look_back + 1):
        df[f'Lag{i}'] = df['Close'].shift(i)
    df['Target'] = df['Close']
    df_clean = df.dropna()
    return df_clean

def write_dzn(df, asset_name, freq_type, lambda_):
    y = df['Target'].values
    X = df[[col for col in df.columns if col.startswith('Lag')]].values
    y_norm = (y - y.mean()) / y.std()
    X_norm = (X - X.mean(axis=0)) / X.std(axis=0)
    filename = f"./dzns/{asset_name}_{freq_type}_regression.dzn"
    with open(filename, 'w') as f:
        f.write(f"n_samples = {len(y_norm)};\n")
        f.write(f"n_features = {X_norm.shape[1]};\n")
        f.write(f"lambda = {lambda_};\n")
        f.write("y = [")
        f.write(", ".join([f"{val:.6f}" for val in y_norm]))
        f.write("];\n")
        f.write("X = [|")
        for i, row in enumerate(X_norm):
            if i > 0:
                f.write("\n     |")
            f.write(", ".join([f"{val:.6f}" for val in row]))
        f.write(" |];\n")
    return filename


assets = {
    "Gold": "./data/Gold.csv",
    "Bitcoin": "./data/Bitcoin.csv",
    "Ethereum": "./data/Ethereum.csv"
}

print("Starting data processing...")
for name, path in assets.items():
    print(f"Processing {name}...")
    daily_df, weekly_df = load_and_clean(path, name)
    daily_df.to_csv(f"./csvs/{name}_clean.csv", index=True)

    daily_prepared = prepare_features(daily_df, DAILY_LAGS, 'daily')
    daily_filtered = daily_prepared[daily_prepared.index >= START_DATE]
    daily_dzn = write_dzn(daily_filtered, name, 'daily', LAMBDA)
    daily_new = daily_prepared[daily_prepared.index >= LAG_START_DATE]
    daily_new.to_csv(f"./csvs/{name}_daily_features.csv", index=True)
    print(f"  Daily: {len(daily_filtered)} samples -> {daily_dzn}")

