import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "BAA Corporate Bond Yield.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "BAA Corporate Bond Yield.csv")

# Load and sort the data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Monthly yield level (last observation)
monthly_last = df.resample("M").last()

# Monthly yield volatility (standard deviation)
monthly_vol = df.resample("M").std()
monthly_vol.columns = ["Volatility"]

# Combine and forward-fill
df_combined = pd.concat([monthly_last, monthly_vol], axis=1).ffill()

# Round both columns to 4 decimal places
df_cleaned = df_combined.round(4)

# Save the cleaned output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
