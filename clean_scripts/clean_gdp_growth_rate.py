import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "GDP Growth Rate.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "GDP Growth Rate.csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# GDP growth is quarterly; simulate actual release time by shifting 3 months forward
df.index = df.index + pd.offsets.QuarterEnd(0) + pd.DateOffset(months=3)

# Optional: Resample to monthly frequency with forward-fill
df_monthly = df.resample("M").ffill().round(2)

# Save cleaned data
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_monthly.to_csv(OUTPUT_FILE)

print(f"Saved GDP Growth Rate with release lag to: {OUTPUT_FILE}")
