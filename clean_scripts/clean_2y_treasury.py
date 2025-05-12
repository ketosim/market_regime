import pandas as pd

# Load the raw series
file_path = "fred_series/2Y Treasury.csv"
df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# This series is already monthly and real-time, so:
# 1. Set to end-of-month for consistency with other series
df.index = df.index.to_period('M').to_timestamp('M')

# 2. Forward-fill any missing values
df_cleaned = df.ffill()

# 3. Save to cleaned folder
output_path = "fred_series_clean/2Y Treasury.csv"
df_cleaned.to_csv(output_path)

print(f"Saved cleaned series to: {output_path}")
