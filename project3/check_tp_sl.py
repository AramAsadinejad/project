import pandas as pd
from datetime import timedelta
import json

def check_tp_sl_and_calculate_profit(input_date, filename, days, tp, sl, type):
    df = pd.read_csv(filename)
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
    input_date = pd.to_datetime(input_date).normalize()

    # چک کردن 7 یا 28 روز آینده
    for i in range(1, days + 1):
        current_date = input_date + timedelta(days=i)
        row = df[df['Date'] == current_date]
        if not row.empty:
            close_price = row['Close'].iloc[0]
            if close_price >= tp or close_price <= sl:
                return calculate_profit(type, close_price)
    
    return None


def calculate_profit(type,closed_price):
    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    count = 0
    if type=="bit_spot":
        count = data.get("bit_spot")[0]
    elif type=="eth_spot":
        count = data.get("eth_spot")[0]

    return count * closed_price