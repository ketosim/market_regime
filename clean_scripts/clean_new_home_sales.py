import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "New Home Sales.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "New Home Sales.csv")

# Load and sort data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Align to end-of-month
df.index = df.index.to_period("M").to_timestamp("M")

# Apply 2-month lag to simulate publication delay
df_shifted = df.shift(2)

# Forward-fill and round to nearest unit
df_cleaned = df_shifted.asfreq("M").ffill().round(0)

# Save cleaned data
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
