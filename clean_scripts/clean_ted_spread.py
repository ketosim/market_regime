import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "TED Spread.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "TED Spread.csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Resample to monthly using mean (average financial stress)
df_monthly = df.resample("M").mean()

# Round to 2 decimals
df_cleaned = df_monthly.ffill().round(2)

# Save cleaned output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
