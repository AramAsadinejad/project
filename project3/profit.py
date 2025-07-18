import json
import csv

def profit_bond_get():
    
    # Load the existing JSON file
    with open("data.json", "r") as f:
        data = json.load(f)

    # Step 1: Read values
    capital = data["capital"]
    last_three_week_bond = data["last_three_week_bond"]
    last_two_week_bond = data["last_two_week_bond"]
    last_week_bond = data["last_week_bond"]

    # Step 2: Update capital
    capital += (last_three_week_bond * 1.0055)
    data["capital"] = capital

    # Step 3: Shift bond values
    data["last_three_week_bond"] = last_two_week_bond
    data["last_two_week_bond"] = last_week_bond
    data["last_week_bond"] = 0

    # Step 4: Save updated data back to JSON
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    #print("✅ JSON updated successfully.")


def shift_json(filepath="data.json"):
    with open(filepath, "r") as f:
        data = json.load(f)

    # === Shift last_two_week to last_three_week ===
    data["last_three_week_bit_l1"] = data["last_two_week_bit_l1"]
    data["last_three_week_bit_l2"] = data["last_two_week_bit_l2"]
    data["last_three_week_bit_l3"] = data["last_two_week_bit_l3"]
    data["last_three_week_eth_l1"] = data["last_two_week_eth_l1"]
    data["last_three_week_eth_l2"] = data["last_two_week_eth_l2"]
    data["last_three_week_eth_l3"] = data["last_two_week_eth_l3"]

    # === Shift last_week to last_two_week ===
    data["last_two_week_bit_l1"] = data["last_week_bit_l1"]
    data["last_two_week_bit_l2"] = data["last_week_bit_l2"]
    data["last_two_week_bit_l3"] = data["last_week_bit_l3"]
    data["last_two_week_eth_l1"] = data["last_week_eth_l1"]
    data["last_two_week_eth_l2"] = data["last_week_eth_l2"]
    data["last_two_week_eth_l3"] = data["last_week_eth_l3"]

    # === Reset last_week values ===
    default_value = [0, 9999999999, 9999999999, 0, 0]
    data["last_week_bit_l1"] = default_value
    data["last_week_bit_l2"] = default_value
    data["last_week_bit_l3"] = default_value
    data["last_week_eth_l1"] = default_value
    data["last_week_eth_l2"] = default_value
    data["last_week_eth_l3"] = default_value

    # === Save the updated JSON ===
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)



def check_tp_sl_triggered(csv_path, json_path, date, target_key):
    # === Load JSON ===
    with open(json_path, "r") as f:
        data = json.load(f)

    # === Load CSV and find the close price for the given date ===
    close_price = None
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Price"] == date:
                close_price = float(row["Close"])
                break

    if close_price is None:
        print(f"❌ Date {date} not found in CSV.")
        return

    # === Extract account values from JSON ===
    account = data[target_key]
    amount = account[0]
    tp = account[1]
    sl = account[2]
    entry_price = account[3]
    is_long = account[4] == 1

    if amount == 0:
        print(f"ℹ️ No active position in {target_key}.")
        return

    # === Determine if TP or SL is hit ===
    tp_hit = (close_price >= tp) if is_long else (close_price <= tp)
    sl_hit = (close_price <= sl) if is_long else (close_price >= sl)

    if tp_hit or sl_hit:
        capital_gain = amount * close_price
        data["capital"] += capital_gain

        print(f"✅ {'TP' if tp_hit else 'SL'} hit for {target_key} on {date}.")
        print(f"📈 Added {capital_gain:.2f} to capital.")

        # Reset account
        data[target_key] = [0, 9999999999, 9999999999, 0, 0]

        # Save updated JSON
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)

    else:
        print(f"⏳ No TP/SL hit for {target_key} on {date}. Close = {close_price}, TP = {tp}, SL = {sl}")

