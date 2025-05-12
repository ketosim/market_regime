import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "Building Permits.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "Building Permits.csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Align index to end-of-month
df.index = df.index.to_period("M").to_timestamp("M")

# Simulate publication delay by shifting 1 month
df_shifted = df.shift(1)

# Ensure consistent monthly index and forward fill
df_cleaned = df_shifted.asfreq("M").ffill()

# Save the cleaned output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
