import pandas as pd
from datetime import datetime, timedelta
import json
def get_bonds_list(date):
    # df = pd.read_csv("transactions.csv")
    # bonds_list = []
    # df['Date'] = pd.to_datetime(df['Date'])
    
    # # شروع از تاریخ ورودی
    # date = pd.to_datetime(date)

    # for i in range(3):
    #     # فیلتر بر اساس تاریخ و نوع
    #     filtered = df[(df['Date'] == date) & (df['type'].str.lower() == 'bonds')]
        
    #     if not filtered.empty:
    #         return float(filtered.iloc[0]['price'])

    #     # رفتن به ۷ روز قبل‌تر
    #     date -= timedelta(days=7)
    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    bonds_list = [0,0,0,0]
    bonds_list[1] = data.get("last_week_bond")
    bonds_list[2] = data.get("last_two_week_bond")
    bonds_list[3] = data.get("last_three_week_bond")
