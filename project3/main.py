from regression import regression
import pandas as pd
from gold_invest_day import get_next_day_price

date = "2025-2-25"
test_df = pd.read_csv("Goldtest.csv", parse_dates=['Date'])
start_date = test_df['Date'].min().strftime('%Y-%m-%d')

regression("Goldtrain.csv","Goldtest.csv",start_date)
regression("Ethereumtrain.csv","Ethereumtest.csv",start_date)
regression("Bitcointrain.csv","Bitcointest.csv",start_date)
regression("Ethereumtrain.csv","Ethereumtest.csv",start_date,28)
regression("Bitcointrain.csv","Bitcointest.csv",start_date,28)



current_start = pd.to_datetime(start_date)

# حداکثر تاریخ در فایل برای جلوگیری از حلقه بی‌نهایت (اختیاری)
max_date = test_df['Date'].max()

while current_start <= max_date:
    # بازه 7 روزه
    current_end = current_start + timedelta(days=6)

    # فیلتر کردن ردیف‌هایی که تاریخشون تو این بازه هست
    mask = (test_df['Date'] >= current_start) & (test_df['Date'] <= current_end)
    filtered = test_df.loc[mask]

    if not filtered.empty:
        pass
    else:
        get_next_day_price(current_start)

    # به بازه بعدی 7 روز اضافه کن
    current_start = current_start + timedelta(days=7)

