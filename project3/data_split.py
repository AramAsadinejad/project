import pandas as pd

# خواندن فایل اصلی
df = pd.read_csv('Bitcoin.csv')

# تقسیم به دو بخش
mid_index = 1220

df_part1 = df.iloc[:mid_index]
df_part2 = df.iloc[mid_index:]

# ذخیره در دو فایل جداگانه
df_part1.to_csv('Bitcointrain.csv', index=False)
df_part2.to_csv('Bitcointest.csv', index=False)

print(f"✅ فایل به دو بخش تقسیم شد: {len(df_part1)} سطر در part1.csv و {len(df_part2)} سطر در part2.csv")
