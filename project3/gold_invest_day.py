import pandas as pd

def get_next_day_price(date):
    input_date = pd.to_datetime(date)
    df = pd.read_csv("Goldtest.csv", parse_dates=["Date"])  # مطمئن شو ستون Date datetime هست

    # مرتب‌سازی بر اساس ستون 'Date'
    df = df.sort_values(by="Date").reset_index(drop=True)

    # پیدا کردن سطرهایی که تاریخشون بزرگتر از input_date باشه (یعنی روزهای بعد)
    future_rows = df[df["Date"] > input_date]

    if future_rows.empty:
        print("تاریخ بعد از تاریخ ورودی وجود ندارد.")
        return None

    # اولین سطر بعد از input_date
    next_row = future_rows.iloc[0]

    next_date = next_row["Date"]
    next_price = next_row["Close"]

    print(f"تاریخ بعد از {date}، برابر است با {next_date.strftime('%Y-%m-%d')} با قیمت {next_price}")
    return next_price
