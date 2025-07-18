import json

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

     
    