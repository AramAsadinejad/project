import pandas as pd
import datetime
import calendar

def load_available_dates():
    all_dates = set()
    for asset in ["Bitcoin", "Ethereum", "Gold"]:
        df = pd.read_csv(f"./data/{asset}.csv", usecols=["Date"])
        df["Date"] = pd.to_datetime(df["Date"])
        all_dates.update(df["Date"].dt.date)
    return sorted(all_dates)

def find_valid_decision_date(monday, available_dates):
    week_range = [monday + datetime.timedelta(days=offset) for offset in range(-3, 4)]
    valid_dates = [d for d in week_range if d in available_dates]
    if not valid_dates:
        return None
    return min(valid_dates, key=lambda d: abs((d - monday).days))

start_date = datetime.date(2024, 4, 1)
end_date = datetime.date(2025, 2, 28)

available_dates = load_available_dates()
decision_dates = []

current = start_date
while current <= end_date:
    while current.weekday() != calendar.MONDAY:
        current += datetime.timedelta(days=1)

    valid_date = find_valid_decision_date(current, available_dates)
    if valid_date:
        decision_dates.append(valid_date)
    #Skip week otherwise
    current += datetime.timedelta(weeks=1)

with open("all_decision_dates.dzn", "w") as f:
    f.write(f"n_weeks = {len(decision_dates)};\n")
    f.write("decision_dates = [")
    f.write(", ".join(f"\"{d.strftime('%Y-%m-%d')}\"" for d in decision_dates))
    f.write("];\n")

print(f"\n Wrote {len(decision_dates)} decision dates to all_decision_dates.dzn")
