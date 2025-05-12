import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "Real GDP.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "Real GDP.csv")

# Load and sort
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Shift timestamps to quarter end, then add ~3-month lag to reflect release
df.index = df.index + pd.offsets.QuarterEnd(0) + pd.DateOffset(months=3)

# Optionally resample monthly and forward fill
df_monthly = df.resample("M").ffill().round(3)

# Save
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_monthly.to_csv(OUTPUT_FILE)

print(f"Saved release-lagged GDP to: {OUTPUT_FILE}")
