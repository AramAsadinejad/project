# main.py
from forecasting.forecast import forecast_prices
from optimization.run_optimization import run_optimization

if __name__ == "__main__":
    gold = forecast_prices("data/gold.csv", 4)
    btc = forecast_prices("data/bitcoin.csv", 4)
    eth = forecast_prices("data/ethereum.csv", 4)

    result = run_optimization(
        gold['Predicted_Close'].tolist(),
        btc['Predicted_Close'].tolist(),
        eth['Predicted_Close'].tolist(),
        weeks=4
    )

    print(result)
