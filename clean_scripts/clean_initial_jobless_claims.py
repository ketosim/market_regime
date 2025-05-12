import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "Initial Jobless Claims.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "Initial Jobless Claims.csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Resample to monthly average
df_monthly = df.resample("M").mean()

# Round to nearest thousand
df_cleaned = df_monthly.ffill().round(-3)

# Save cleaned output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
