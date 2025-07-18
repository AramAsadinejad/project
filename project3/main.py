from regression import regression, compare_and_save_best_predictions
import pandas as pd
from gold_invest_day import get_next_day_price
from minizinc_runner2 import run
import json
from bond_list import get_bonds_list
from datetime import datetime, timedelta
from day_price import get_price_of_day
from tpsl import tpsl
from check_tp_sl import check_tp_sl_and_calculate_profit


date = "2025-4-24"
test_df = pd.read_csv("Goldtest.csv", parse_dates=['Date'])
start_date = test_df['Date'].min().strftime('%Y-%m-%d')

regression("Goldtrain.csv","Goldtest.csv",start_date)
regression("Ethereumtrain.csv","Ethereumtest.csv",start_date)
regression("Bitcointrain.csv","Bitcointest.csv",start_date)
regression("Ethereumtrain.csv","Ethereumtest.csv",start_date,28)
regression("Bitcointrain.csv","Bitcointest.csv",start_date,28)


compare_and_save_best_predictions("Gol_predicted_from_2025-01-02.csv", "Goldtest.csv")
compare_and_save_best_predictions("Eth_predicted_from_2025-01-02.csv", "Ethereumtest.csv", "Eth_filtered.csv")
compare_and_save_best_predictions("Bit_predicted_from_2025-01-02.csv", "Bitcointest.csv", "Bit_filtered.csv")



current_start = pd.to_datetime(start_date)
with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

capital = data.get("capital")


max_date = test_df['Date'].max()

while current_start <= max_date:

    # filtered = test_df[test_df[date] == current_start]
    filtered = test_df[test_df['Date'] == current_start]
    c_g = ""
    eth_result = tpsl(current_start, current_start + timedelta(days=7),
                  "Ethereumtest.csv","Eth_filtered.csv")
    bit_result = tpsl(current_start, current_start + timedelta(days=7),
                  "Bitcointest.csv","Bit_filtered.csv")
    ethm_result = tpsl(current_start, current_start + timedelta(days=28),
                  "Ethereumtest.csv","eth_filtered.csv")
    bitm_result = tpsl(current_start, current_start + timedelta(days=28),
                  "Bitcointest.csv","bit_filtered.csv")

    if not filtered.empty:
        c_g = get_price_of_day("Goldtest.csv",current_start)
    else:
        c_g = get_next_day_price(current_start)

    tpsl_eth_spot_flag = check_tp_sl_and_calculate_profit(current_start,"Ethereumtest.csv",7
                                                 ,eth_result["TP"], eth_result["SL"],"eth_spot")
    tpsl_bit_spot_flag = check_tp_sl_and_calculate_profit(current_start,"Bitcointest.csv",7
                                                 ,bit_result["TP"], bit_result["SL"],"bit_spot")
    tpsl_eth_m_flag = check_tp_sl_and_calculate_profit(current_start,"Ethereumtest.csv",28
                                                 ,ethm_result["TP"], ethm_result["SL"],"eth_spot")
    tpsl_bit_m_flag = check_tp_sl_and_calculate_profit(current_start,"Bitcointest.csv",28
                                                 ,bitm_result["TP"], bitm_result["SL"],"bit_spot")
         
    print(capital)
    filtered = pd.read_csv("filtered_predictions.csv")
    p_g = filtered["Best_Prediction"].iloc[-1]
    run(capital=capital*95/100,bonds=get_bonds_list(current_start),
            c_g=c_g, c_b=get_price_of_day("Bitcointest.csv",current_start),
            c_e=get_price_of_day("Ethereumtest.csv",current_start),
            p_g=p_g,
            p_b=bit_result['TP']+get_price_of_day("Bitcointest.csv",current_start),
            p_e=eth_result['TP']+get_price_of_day("Ethereumtest.csv",current_start),
            p_bm=bitm_result['TP']+get_price_of_day("Bitcointest.csv",current_start),
            p_em=ethm_result['TP']+get_price_of_day("Ethereumtest.csv",current_start),
    )

    current_start = current_start + timedelta(days=7)

