# forecasting/forecast.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

def forecast_prices(csv_file, forecast_weeks=4):
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    df['Week'] = np.arange(len(df))
    X = df[['Week']]
    y = df['Close']

    model = LinearRegression()
    model.fit(X, y)

    future_weeks = np.arange(len(df), len(df) + forecast_weeks).reshape(-1, 1)
    predictions = model.predict(future_weeks)

    last_date = df['Date'].iloc[-1]
    future_dates = [last_date + timedelta(weeks=i + 1) for i in range(forecast_weeks)]

    return pd.DataFrame({'Date': future_dates, 'Predicted_Close': predictions})
