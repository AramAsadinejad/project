import pandas as pd

def get_price_of_day(filename, date):
    print(date)
    df = pd.read_csv(filename)
    date = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    price = df[df["Date"] == date]["Close"].iloc[0]
    return price
