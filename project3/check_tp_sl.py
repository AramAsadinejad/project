import pandas as pd
from datetime import timedelta

def check_tp_sl_and_calculate_profit(input_date, filename, days, tp, sl):
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
                # به سود یا ضرر خوردیم، تابع محاسبه سود رو صدا بزن
                # return calculate_profit_fn(entry_price, close_price, current_date, filename)
    
    # اگر در این بازه هیچکدوم فعال نشدن
    return None
