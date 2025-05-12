import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from hmmlearn import hmm
from datetime import datetime

# === Setup ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("output", exist_ok=True)

# === Load data ===
fred_data = pd.read_csv('fred_master_dataset_2000_onwards.csv', parse_dates=['Date'], index_col='Date')
sector_returns = pd.read_csv('sector_returns_monthly.csv', parse_dates=['Date'], index_col='Date')

# === Feature engineering ===
fred_data['Yield_Curve_Slope'] = fred_data['10Y_Treasury'] - fred_data['2Y_Treasury']
fred_data['IP_YoY'] = fred_data['Industrial_Production_Index'].pct_change(12)
fred_data['Inflation_YoY'] = fred_data['CPI_(All_Items)'].pct_change(12)

selected_indicators = [
    'TED_Spread', '10Y_Treasury', 'Leading_Economic_Index', 'Initial_Jobless_Claims',
    'Capacity_Utilization', 'Industrial_Production_Index', 'Core_CPI',
    'Exports_(Goods_&_Services)', 'PCE_Price_Index', 'CPI_(All_Items)',
    'High_Yield_Spread_(ICE_BofA)', '2Y_Treasury', 'Personal_Consumption_Expenditures',
    'PPI_(All_Commodities)', 'BAA_Corporate_Bond_Yield_Bond_BAA_Yield_Volatility'
]

fred_data.index = fred_data.index.to_period('M').to_timestamp()
sector_returns.index = sector_returns.index.to_period('M').to_timestamp()
common_index = fred_data.index.intersection(sector_returns.index)

macro_aligned = fred_data.loc[common_index, selected_indicators].copy()
macro_aligned = macro_aligned.ffill().bfill()

# === Define 70/30 split ===
macro_window = macro_aligned.loc["2000-07-01":"2024-07-01"]
total_months = len(macro_window)
split_index = int(total_months * 0.7)

train_data = macro_window.iloc[:split_index]
predict_data = macro_window.iloc[split_index:]

# Standardize using training scaler
scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_data)
predict_scaled = scaler.transform(predict_data)

# === Loop through regime counts ===
for n_regimes in range(4, 9):
    model = hmm.GaussianHMM(n_components=n_regimes, covariance_type="full", n_iter=100, random_state=42)
    model.fit(train_scaled)

    # Predict only for the 30% test set
    hidden_states = model.predict(predict_scaled)
    regime_probs = model.predict_proba(predict_scaled)

    # === Save regime sequence plot ===
    regime_df = pd.DataFrame({"Date": predict_data.index, "Regime": hidden_states}).set_index("Date")
    plt.figure(figsize=(12, 4))
    plt.plot(regime_df.index, regime_df['Regime'], drawstyle='steps-post')
    plt.title(f'HMM Predicted Regimes (2000-2024)\nTrained on first 70%, Predicted on last 30% (n={n_regimes})')
    plt.xlabel("Date")
    plt.ylabel("Regime")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'output/rolling_pred_30pct_regime_n{n_regimes}_{timestamp}.png')
    plt.close()

    # === Save regime probabilities plot ===
    regime_probs_df = pd.DataFrame(regime_probs, index=predict_data.index, columns=[f'Regime_{i}' for i in range(n_regimes)])
    plt.figure(figsize=(14, 6))
    for i in range(n_regimes):
        plt.plot(regime_probs_df.index, regime_probs_df[f'Regime_{i}'], label=f'Regime {i}')
    plt.title(f'HMM Regime Probabilities (Predicted on last 30%) - n={n_regimes}')
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'output/rolling_pred_30pct_probs_n{n_regimes}_{timestamp}.png')
    plt.close()

    # === Save results to CSV ===
    regime_df.to_csv(f'output/rolling_pred_30pct_regime_n{n_regimes}_{timestamp}.csv')
    regime_probs_df.to_csv(f'output/rolling_pred_30pct_probs_n{n_regimes}_{timestamp}.csv')

print("✅ HMM prediction on last 30% of data (with model trained on first 70%) completed and saved.") 