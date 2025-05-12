import pandas as pd
import os

# File paths
INPUT_FILE = os.path.join("..", "fred_series", "Personal Consumption Expenditures.csv")
OUTPUT_FILE = os.path.join("..", "fred_series_clean", "Personal Consumption Expenditures.csv")

# Load and sort data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
df = df.sort_index()

# Convert index to month-end
df.index = df.index.to_period("M").to_timestamp("M")

# Simulate publication delay: 2 months
df_shifted = df.shift(2)

# Forward-fill and round to whole number (millions)
df_cleaned = df_shifted.asfreq("M").ffill().round(0)

# Save output
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_cleaned.to_csv(OUTPUT_FILE)

print(f"Saved cleaned file to: {OUTPUT_FILE}")
