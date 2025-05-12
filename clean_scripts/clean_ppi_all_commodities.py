import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "PPI (All Commodities).csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "PPI (All Commodities).csv")

# Load and sort data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Convert to end-of-month
df.index = df.index.to_period("M").to_timestamp("M")

# Apply 1-month publication delay
df_shifted = df.shift(1)

# Forward-fill and round
df_cleaned = df_shifted.asfreq("M").ffill().round(2)

# Save cleaned file
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
