import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "3M T-Bill.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "3M T-Bill.csv")

# Load raw data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Resample to monthly frequency using last value in each month
df_monthly = df.resample('M').last()

# No lag needed — this is real-time market data

# Forward fill any missing monthly values
df_cleaned = df_monthly.ffill()

# Save to clean output directory
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Cleaned '3M T-Bill.csv' saved to: {OUTPUT_FILE}")
