import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


#AI Generated, Just for testing purposes
def load_weights(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    weights_match = re.search(r"Weights:\s*\[([^\]]+)\]", content)
    intercept_match = re.search(r"Intercept:\s*([-+]?[0-9]*\.?[0-9]+)", content)

    weights = list(map(float, weights_match.group(1).split(',')))
    intercept = float(intercept_match.group(1))
    return weights, intercept

def evaluate_predictions(csv_path, weights_path, asset_name):
    df = pd.read_csv(csv_path)
    weights, intercept = load_weights(weights_path)

    # Get only Lag features
    lag_cols = [col for col in df.columns if col.startswith("Lag")]
    X = df[lag_cols].values
    y_true = df["Target"].values

    # Compute predictions
    y_pred = np.dot(X, weights) + intercept

    # Compute errors
    abs_error = np.abs(y_true - y_pred)
    sq_error = (y_true - y_pred) ** 2

    mae = abs_error.mean()
    rmse = np.sqrt(sq_error.mean())

    # Combine into a DataFrame for analysis
    result = pd.DataFrame({
        "Actual": y_true,
        "Predicted": y_pred,
        "Absolute Error": abs_error,
        "Squared Error": sq_error
    })

    print(f"\n===== {asset_name} Prediction Summary =====")
    print(f"Total Samples: {len(df)}")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

    print(f"Mean Actual Price:    {y_true.mean():.2f}")
    print(f"Mean Predicted Price: {y_pred.mean():.2f}")
    print(f"MAE as % of Mean:     {(mae / y_true.mean()) * 100:.2f}%")
    print(f"RMSE as % of Mean:    {(rmse / y_true.mean()) * 100:.2f}%")

    plt.plot(y_true, label='Actual')
    plt.plot(y_pred, label='Predicted')
    plt.title(f"{asset_name} - Actual vs Predicted")
    plt.legend()
    plt.show()
        
    # print(result)

    return result

# evaluate_predictions("./csvs/Bitcoin_weekly_features.csv", "./regression_out/Bitcoin_weekly_weights.txt", "Bitcoin")
# evaluate_predictions("./csvs/Ethereum_weekly_features.csv", "./regression_out/Ethereum_weekly_weights.txt", "Ethereum")
# evaluate_predictions("./csvs/Gold_weekly_features.csv", "./regression_out/Gold_weekly_weights.txt", "Gold")
evaluate_predictions("./csvs/Bitcoin_daily_features.csv", "./regression_out/Bitcoin_daily_weights.txt", "Bitcoin")
evaluate_predictions("./csvs/Ethereum_daily_features.csv", "./regression_out/Ethereum_daily_weights.txt", "Ethereum")
evaluate_predictions("./csvs/Gold_daily_features.csv", "./regression_out/Gold_daily_weights.txt", "Gold")
