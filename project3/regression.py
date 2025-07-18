import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def regression(train_file, test_file, start_date_str, predict_days=7):
    # خواندن داده‌ها
    train_df = pd.read_csv(train_file, parse_dates=['Date'])
    test_df = pd.read_csv(test_file, parse_dates=['Date'])
    

    # مرتب‌سازی و ریست ایندکس
    train_df = train_df.sort_values(by='Date').reset_index(drop=True)
    test_df = test_df.sort_values(by='Date').reset_index(drop=True)

    # افزودن ایندکس و روز هفته به هر دیتافریم
    train_df['DayIndex'] = np.arange(len(train_df))
    train_df['Weekday'] = train_df['Date'].dt.dayofweek
    test_df['DayIndex'] = np.arange(len(train_df), len(train_df) + len(test_df))
    test_df['Weekday'] = test_df['Date'].dt.dayofweek

    # مدل 1: Linear Regression
    model1 = LinearRegression()
    model1.fit(train_df[['DayIndex']], train_df['Close'])
    test_df['predicted1'] = model1.predict(test_df[['DayIndex']])
    mse1 = mean_squared_error(test_df['Close'], test_df['predicted1'])

    # مدل 2: Residual-enhanced
    train_df['residual'] = train_df['Close'] - model1.predict(train_df[['DayIndex']])
    model2 = LinearRegression()
    model2.fit(train_df[['DayIndex']], train_df['residual'])
    test_df['residual_pred'] = model2.predict(test_df[['DayIndex']])
    test_df['predicted2'] = test_df['predicted1'] + test_df['residual_pred']
    mse2 = mean_squared_error(test_df['Close'], test_df['predicted2'])

    # مدل 3: میانگین روز هفته (بر اساس train)
    weekday_avg = train_df.groupby('Weekday')['Close'].mean().to_dict()
    overall_avg = train_df['Close'].mean()
    test_df['predicted3'] = test_df['Weekday'].map(lambda d: weekday_avg.get(d, overall_avg))
    mse3 = mean_squared_error(test_df['Close'], test_df['predicted3'])

    # پیش‌بینی بازه زمانی دلخواه

    start_date = pd.to_datetime(start_date_str)
    base_date = train_df['Date'].min()

    future_dates = pd.date_range(start=start_date, periods=predict_days)
    future_days = [(date - base_date).days for date in future_dates]

    predicted1_future = model1.predict(np.array(future_days).reshape(-1, 1))
    predicted2_future = predicted1_future + model2.predict(np.array(future_days).reshape(-1, 1))
    predicted3_future = [weekday_avg.get(date.dayofweek, overall_avg) for date in future_dates]

    # خروجی دیتافریم پیش‌بینی
    future_df = pd.DataFrame({
        'Date': future_dates,
        'Weekday': future_dates.day_name(),
        'Predicted_Close_Simple': predicted1_future,
        'Predicted_Close_Residual': predicted2_future,
        'Predicted_Close_WeekdayAverage': predicted3_future
    })

    future_df.to_csv(f"{train_file[0:3]}_predicted_from_{start_date_str}.csv", index=False)
    print(f"✅ پیش‌بینی برای {predict_days} روز از {start_date_str} ذخیره شد.")
    print(future_df)

    # رسم نمودار کل داده‌ها و پیش‌بینی
    # plt.figure(figsize=(14, 6))

    # plt.plot(train_df['Price'], train_df['Close'], label='Train Actual', color='black')
    # plt.plot(test_df['Price'], test_df['Close'], label='Test Actual', color='gray')
    # plt.plot(test_df['Price'], test_df['predicted1'], label='Test Predicted Linear', linestyle='--', color='blue')
    # plt.plot(test_df['Price'], test_df['predicted2'], label='Test Predicted Residual', linestyle='--', color='green')
    # plt.plot(test_df['Price'], test_df['predicted3'], label='Test Predicted Weekday Avg', linestyle='--', color='orange')

    # plt.plot(future_dates, predicted1_future, label='Future Predicted Linear', color='blue')
    # plt.plot(future_dates, predicted2_future, label='Future Predicted Residual', color='green')
    # plt.plot(future_dates, predicted3_future, label='Future Predicted Weekday Avg', color='orange')

    # plt.xlabel('Date')
    # plt.ylabel('Close Price')
    # plt.title(f'Forecast from {start_date_str} for {predict_days} days')
    # plt.legend()
    # plt.grid(True)
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()
