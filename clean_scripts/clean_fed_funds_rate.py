import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "Fed Funds Rate.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "Fed Funds Rate.csv")

# Load and sort data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Align index to end-of-month
df.index = df.index.to_period("M").to_timestamp("M")

# No shift needed — real-time rate
df_cleaned = df.asfreq("M").ffill()

# Save cleaned file
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
