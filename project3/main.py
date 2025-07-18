from regression import regression
import pandas as pd
from gold_invest_day import get_next_day_price
from minizinc_runner import run
import json
from bond_list import get_bonds_list
from datetime import datetime, timedelta
from day_price import get_price_of_day

date = "2025-4-24"
test_df = pd.read_csv("Goldtest.csv", parse_dates=['Date'])
start_date = test_df['Date'].min().strftime('%Y-%m-%d')

regression("Goldtrain.csv","Goldtest.csv",start_date)
regression("Ethereumtrain.csv","Ethereumtest.csv",start_date)
regression("Bitcointrain.csv","Bitcointest.csv",start_date)
regression("Ethereumtrain.csv","Ethereumtest.csv",start_date,28)
regression("Bitcointrain.csv","Bitcointest.csv",start_date,28)



current_start = pd.to_datetime(start_date)
with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

capital = data.get("Capital")


max_date = test_df['Date'].max()

while current_start <= max_date:

    # filtered = test_df[test_df[date] == current_start]
    filtered = test_df[test_df['Date'] == current_start]
    c_g = ""
    if not filtered.empty:
        c_g = get_price_of_day("Goldtest.csv",current_start)
    else:
        c_g = get_next_day_price(current_start)
    
    run(capital=capital*95/100,bonds=get_bonds_list(current_start),
            c_g=c_g, b_g=get_price_of_day("Bitcoin.csv",current_start),
            e_g=get_price_of_day("Ethereum.csv",current_start),
    )

    current_start = current_start + timedelta(days=7)

