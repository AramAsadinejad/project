import pandas as pd

def profit(csv_file):
    df = pd.read_csv(csv_file)

    # محاسبه min و max ستون قیمت
    min_price = df[Predicted_Close_Simple].min()
    max_price = df[Predicted_Close_Simple].max()

    print(f"کمترین قیمت در ستون '{price_column}': {min_price}")
    print(f"بیشترین قیمت در ستون '{price_column}': {max_price}")

    # خواندن فایل JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # اگر کلید مشخص شده بود، مقدارش رو بگیر
    if json_key:
        value = data.get(Capital, None)
        if value is not None:
            print(f"مقدار کلید '{json_key}' در JSON: {value}")
        else:
            print(f"کلید '{json_key}' در فایل JSON پیدا نشد.")
    else:
        print("کلیدی برای خواندن از JSON داده نشده است.")
    
    # اگه خواستی می‌تونی min و max رو برگردونی:
    return stop_loss, take_profit