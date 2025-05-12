import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "CPI (All Items).csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "CPI (All Items).csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Convert to month-end for alignment
df.index = df.index.to_period("M").to_timestamp("M")

# Apply 1-month publication lag
df_shifted = df.shift(1)

# Forward-fill any missing values
df_cleaned = df_shifted.asfreq("M").ffill()

# Save the cleaned output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
