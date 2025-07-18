import pandas as pd

def get_next_day_price(date):
    input_date = pd.to_datetime(date)
    df = pd.read_csv("Goldtest.csv")
    # مرتب‌سازی بر اساس تاریخ
    df = df.sort_values(by=date).reset_index(drop=True)

    # پیدا کردن سطرهایی که تاریخ بزرگتر از input_date هستند (یعنی روز بعد یا بعدتر)
    future_rows = df[df[date] > input_date]

    if future_rows.empty:
        print("تاریخ بعد از تاریخ ورودی وجود ندارد.")
        return None

    next_row = future_rows.iloc[0]

    next_date = next_row["Date"]
    next_price = next_row["Price"]

    print(f"تاریخ بعد از {date}، برابر است با {next_date.strftime('%Y-%m-%d')} با قیمت {next_price}")
    return next_price


