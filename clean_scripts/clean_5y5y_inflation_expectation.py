import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "5Y5Y Inflation Expectation.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "5Y5Y Inflation Expectation.csv")

# Load and sort data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Resample: last value for level, std for volatility
monthly_last = df.resample('M').last()
monthly_vol = df.resample('M').std()
monthly_vol.columns = ['Volatility']

# Combine
df_cleaned = pd.concat([monthly_last, monthly_vol], axis=1)

# Forward-fill and round to 3 decimal places
df_cleaned = df_cleaned.ffill().round(3)

# Save cleaned output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned series with volatility (rounded to 3 dp) to: {OUTPUT_FILE}")
