import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "AAA Corporate Bond Yield.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "AAA Corporate Bond Yield.csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Monthly yield level: last value of each month
monthly_last = df.resample("M").last()

# Monthly yield volatility: standard deviation within the month
monthly_vol = df.resample("M").std()
monthly_vol.columns = ["Volatility"]

# Combine and forward-fill
df_combined = pd.concat([monthly_last, monthly_vol], axis=1).ffill()

# Round to 4 decimal places
df_cleaned = df_combined.round(4)

# Save
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
