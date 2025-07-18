#!/bin/bash

#Clean up previous outputs except data, Python, MZN, and SH files
find . -type f ! -name "*.py" ! -name "*.sh" ! -name "*.mzn" ! -path "./data/*" ! -path "./oldies/*" -exec rm -f {} +

#Create output folders
mkdir -p dzns
mkdir -p csvs
mkdir -p regression_out

python ./data_clean.py

for asset in Bitcoin Ethereum Gold; do
    # dzn_weekly_path="./dzns/${asset}_weekly_regression.dzn"
    # out_weekly_path="./regression_out/${asset}_weekly_weights.txt"
    dzn_daily_path="./dzns/${asset}_daily_regression.dzn"
    out_daily_path="./regression_out/${asset}_daily_weights.txt"
    echo "Running regression for $asset..."
    # minizinc --solver cbc lasso_regression.mzn "$dzn_weekly_path" > "$out_weekly_path"
    minizinc --solver cbc lasso_regression.mzn "$dzn_daily_path" > "$out_daily_path"

done

echo "Getting valid dates..."
python ./date_generator.py

echo "Simulating portfolio..."
python ./simulate_portfolio.py
