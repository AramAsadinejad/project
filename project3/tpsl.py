import pandas as pd

def tpsl(start_date, future_date, reference_file, future_file):
    # Load data
    ref_df = pd.read_csv(reference_file, parse_dates=['Date'])
    fut_df = pd.read_csv(future_file, parse_dates=['Date'])

    # Get entry (close) price
    ref_row = ref_df[ref_df['Date'] == pd.to_datetime(start_date)]
    if ref_row.empty:
        raise ValueError(f"❌ No data found for start_date: {start_date} in {reference_file}")
    entry_price = ref_row['Close'].values[0]

    # Filter future data within the desired date range
    mask = (fut_df['Date'] > pd.to_datetime(start_date)) & (fut_df['Date'] <= pd.to_datetime(future_date))
    fut_window = fut_df.loc[mask].copy()
    
    if fut_window.empty:
        raise ValueError(f"❌ No future data between {start_date} and {future_date} found.")

    # Prices above and below the entry price
    above = fut_window[fut_window['Price'] > entry_price]
    below = fut_window[fut_window['Price'] < entry_price]

    if above.empty and below.empty:
        raise ValueError("⚠️ No prices above or below the entry price in the given range.")

    # Max above → potential TP for long
    max_above = above.loc[above['Close'].idxmax()] if not above.empty else None

    # Min below → potential TP for short
    min_below = below.loc[below['Close'].idxmin()] if not below.empty else None

    # Compare which is further
    distance_above = abs(max_above['Close'] - entry_price) if max_above is not None else -1
    distance_below = abs(min_below['Close'] - entry_price) if min_below is not None else -1

    if distance_above > distance_below:
        TP = max_above['Close']
        TP_date = max_above['Date']
        SL = min_below['Close'] if min_below is not None else entry_price
        SL_date = min_below['Date'] if min_below is not None else None
        isLong = True
    else:
        TP = min_below['Close']
        TP_date = min_below['Date']
        SL = max_above['Close'] if max_above is not None else entry_price
        SL_date = max_above['Date'] if max_above is not None else None
        isLong = False

    # Return result
    return {
        'TP': TP,
        'TP_date': TP_date,
        'SL': SL,
        'SL_date': SL_date,
        'entry_price': entry_price,
        'isLong': isLong
    }
