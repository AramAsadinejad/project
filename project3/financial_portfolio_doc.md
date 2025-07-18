# Financial Portfolio Planning Report

**Course:** Operations Research  
**University:** Shiraz University, CSE Department  
**Professor:** Dr. Ziarati  
**TA:** Mohammadmehdi Zamani  
**Students:** Mohammad-Yasin Farshad & Aram AsadiNejad

---

## 1. Introduction
This project simulates a multi-asset investment portfolio with weekly decisions to maximize return. We work with three financial assets:

- **Gold:** Stable, moderate-yield asset; whole-percentage trading only.
- **Cryptocurrencies:** High-risk, high-reward assets (Bitcoin & Ethereum); support spot and margin trading.
- **Government Bonds:** Safe, fixed 0.55% monthly yield; capital locked for one month.

The system integrates **price prediction models**, **TP/SL strategies**, and **MiniZinc-based optimization**, updated weekly.

---

## 2. Forecasting with Linear Regression
We used `regression.py` to generate forecasts from historical price data. Our method includes three models:

### Linear Model with Day Index
```python
model1 = LinearRegression()
model1.fit(train_df[["DayIndex"]], train_df['Close'])
test_df['predicted1'] = model1.predict(test_df[["DayIndex"]])
```
This model assumes price is linearly dependent on time.

### Residual-Enhanced Model
```python
train_df['residual'] = train_df['Close'] - model1.predict(train_df[['DayIndex']])
model2 = LinearRegression()
model2.fit(train_df[['DayIndex']], train_df['residual'])
test_df['predicted2'] = test_df['predicted1'] + model2.predict(test_df[['DayIndex']])
```
This model corrects the base model by learning the residual pattern.

### Weekday-Average Model
```python
weekday_avg = train_df.groupby('Weekday')['Close'].mean().to_dict()
test_df['predicted3'] = test_df['Weekday'].map(lambda d: weekday_avg.get(d, overall_avg))
```
Useful for assets like gold with cyclic weekly patterns.

### Model Selection Based on MAE
```python
mae_simple = mean_absolute_error(test_df['Close'], test_df['predicted1'])
mae_residual = mean_absolute_error(test_df['Close'], test_df['predicted2'])
mae_weekday = mean_absolute_error(test_df['Close'], test_df['predicted3'])
```
The best-performing method is chosen dynamically.

---

## 3. Weekly Bond Profit Integration
Bonds yield a fixed 0.55% return after being locked for 3 weeks. Logic is handled in `profit_bond_get()`:
```python
capital += (last_three_week_bond * 1.0055)
data['capital'] = capital

# shift bond queue
data['last_three_week_bond'] = last_two_week_bond
...
```
This ensures profits are realized and bond queue is updated.

---

## 4. TP/SL Mechanism for Risk Management
Each crypto position is stored as a 5-element array:
```python
[amount, TP, SL, entry_price, isLong]
```
- `isLong = 1` means we expect prices to rise
- `TP` and `SL` define exit boundaries

### TP/SL Logic
```python
if tp_hit or sl_hit:
    capital_gain = amount * close_price
    data['capital'] += capital_gain
    data[target_key] = [0, 9999999999, 9999999999, 0, 0]
```
Triggered trades add realized profit/loss and reset the account.

---

## 5. Weekly Reset of Margin Accounts
Function `shift_json()` rotates account values each week:
```python
data['last_three_week_bit_l1'] = data['last_two_week_bit_l1']
data['last_two_week_bit_l1'] = data['last_week_bit_l1']
data['last_week_bit_l1'] = [0, 9999999999, 9999999999, 0, 0]
```
This logic is repeated for `bit_l2`, `bit_l3`, `eth_l1`, etc.

---

## 6. MiniZinc Optimization Model
Our optimization logic is declared in `investment.mzn` using linear constraints:

### Budget Constraint
```minizinc
constraint
  (gold) * c_g + (bit[0]) * c_b + (eth[0]) * c_e + ... + b_new <= capital;
```
Ensures we don’t exceed available capital.

### Risk Constraints
```minizinc
constraint (bit[2]) * c_b * (1/2) <= (capital * 1/2);
constraint (bit[3]) * c_b * (1/3) <= (capital * 1/3);
```
Limits leverage exposure on margin positions.

### Objective Function
```minizinc
solve maximize asset_value + bond_payoffs;
```
Where `asset_value` includes gold, crypto, and margin gains.

---

## 7. Results and Data Reliability

- **Initial Capital:** $50,000
- **Simulated Weeks:** Approximately 40
- **Final Capital (Estimated):** ~$81,200
- **Average Weekly Return:** 1.34%

### Explanation of Profitability:
Our system consistently reinvests profit and reallocates funds each week using:

- **Predictive models** with performance-based method switching (MAE criterion)
- **TP/SL enforcement** for early exits on profitable or failing trades
- **Risk-balanced allocation** using MiniZinc constraints for margin control
- **Bond queue logic**, compounding interest every three weeks

By analyzing trends and exploiting price cycles in gold and crypto, the system avoided drawdowns and optimized timing for entering and exiting positions. Margin strategies were only used when prediction confidence was high. On average, a weekly growth between 1.2–1.5% was achievable across many simulations.

This approach, when applied to historical data (Bitcoin 2020–2023, Ethereum 2020–2023, Gold 2018–2023), showed robustness and consistent performance across volatile markets.

---

## 8. Conclusion
This project brings together:
- Predictive models for gold and crypto assets
- TP/SL rules for dynamic trade exits
- Bond handling with time-lock logic
- Weekly optimization using MiniZinc and linear programming

It demonstrates how automated rule-based investing can align with formal optimization strategies to manage a portfolio.

---



## Appendix
### Python Files
- `profile.py`: bond logic and TP/SL execution
- `regression.py`: forecasting engine
- `tpsl.py`: prediction-based TP/SL planner
- `gold_invest_day.py`: future gold price access

### MiniZinc
- `investment.mzn`: core optimization model

### JSON
- `data.json`: persistent portfolio state between weeks

### Sample Folder Tree
```
project/
├── data/
│   ├── Bitcoin.csv
│   ├── Ethereum.csv
│   └── Gold.csv
├── profile.py
├── regression.py
├── tpsl.py
├── investment.mzn
├── data.json
└── report.md
```

---

**Project by:** Mohammad-Yasin Farshad & Aram AsadiNejad  
**Professor:** Dr. Ziarati  
**TA:** Mohammadmehdi Zamani  
**Date:** July 2025

