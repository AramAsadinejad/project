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
    


def compare_and_save_best_predictions(predictions_file, actuals_file, output_file='filtered_predictions.csv'):
    # Load predictions and actuals
    pred_df = pd.read_csv(predictions_file, parse_dates=['Date'])
    actuals_df = pd.read_csv(actuals_file, parse_dates=['Price'])

    # Rename columns for merging
    actuals_df = actuals_df.rename(columns={'Price': 'Date', 'Close': 'Actual_Close'})

    # Merge on 'Date'
    merged_df = pd.merge(pred_df, actuals_df[['Date', 'Actual_Close']], on='Date', how='inner')

    # Calculate absolute errors
    merged_df['Error_Simple'] = (merged_df['Predicted_Close_Simple'] - merged_df['Actual_Close']).abs()
    merged_df['Error_Residual'] = (merged_df['Predicted_Close_Residual'] - merged_df['Actual_Close']).abs()
    merged_df['Error_WeekdayAverage'] = (merged_df['Predicted_Close_WeekdayAverage'] - merged_df['Actual_Close']).abs()

    # Compute MAE
    mae_simple = merged_df['Error_Simple'].mean()
    mae_residual = merged_df['Error_Residual'].mean()
    mae_weekday = merged_df['Error_WeekdayAverage'].mean()

    # Determine best prediction column
    errors = {
        'Predicted_Close_Simple': mae_simple,
        'Predicted_Close_Residual': mae_residual,
        'Predicted_Close_WeekdayAverage': mae_weekday
    }
    best_col = min(errors, key=errors.get)

    print("📊 Mean Absolute Errors:")
    print(f"  - Simple Linear Regression: {mae_simple:.4f}")
    print(f"  - Residual-enhanced Regression: {mae_residual:.4f}")
    print(f"  - Weekday Average: {mae_weekday:.4f}")
    print(f"\n✅ Best prediction method: **{best_col}** (lowest MAE)")

    # Prepare final output: just Date + Best_Prediction
    filtered_df = merged_df[['Date', best_col]].rename(columns={best_col: 'Best_Prediction'})

    # Save to CSV
    filtered_df.to_csv(output_file, index=False)
    print(f"\n💾 Filtered predictions saved to: {output_file}")

    return filtered_df

def filter_by_method(csv_file, method_column_name, output_file='filtered_by_method.csv'):
    # Load the input CSV
    df = pd.read_csv(csv_file, parse_dates=['Date'])

    # Check if the method column exists
    if method_column_name not in df.columns:
        print(f"❌ Column '{method_column_name}' not found in {csv_file}")
        print(f"✅ Available columns: {list(df.columns)}")
        return None

    # Filter to Date and specified method column
    filtered_df = df[['Date', method_column_name]].rename(columns={method_column_name: 'Filtered_Prediction'})

    # Save to CSV
    filtered_df.to_csv(output_file, index=False)
    print(f"\n📁 File saved: {output_file} — filtered by '{method_column_name}'")

    return filtered_df


# Example usage:
# compare_predictions_to_actuals("tra_predicted_from_2025-01-02.csv", "your_actual_data.csv")

compare_and_save_best_predictions("Gol_predicted_from_2025-01-02.csv", "Gold.csv")
