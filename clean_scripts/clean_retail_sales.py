import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "Retail Sales (Ex Auto).csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "Retail Sales (Ex Auto).csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Align to month-end
df.index = df.index.to_period("M").to_timestamp("M")

# Apply 1-month lag to simulate mid-month release
df_shifted = df.shift(1)

# Resample and round
df_cleaned = df_shifted.asfreq("M").ffill().round(0)

# Save
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
