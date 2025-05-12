import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "High Yield Spread (ICE BofA).csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "High Yield Spread (ICE BofA).csv")

# Load and sort data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Resample to monthly using mean (captures overall monthly risk sentiment)
df_monthly = df.resample("M").mean()

# Forward fill any gaps
df_cleaned = df_monthly.ffill().round(2)

# Save output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
