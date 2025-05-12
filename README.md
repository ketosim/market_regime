# Market Regime Detection

This repository contains code for detecting market regimes using Hidden Markov Models (HMM). The project analyses financial market data to identify distinct economic states or "regimes" that occur over time.

## Features

* Time series analysis of financial market data
* Hidden Markov Model implementation for regime detection
* Visualisation of regime probabilities over time
* Correlation with major economic events (2001 recession, 2008 financial crisis, 2020 pandemic)

## Data

The model works with financial time series data such as:
* Market indices (S&P 500, NASDAQ, etc.)
* Economic indicators
* Asset prices or returns

## Methodology

The Hidden Markov Model approach identifies distinct market states by:
1. Learning the transition probabilities between different regimes
2. Capturing the emission probabilities that characterise each regime
3. Using the Viterbi algorithm to determine the most likely sequence of regimes

## Applications

* Market timing strategies
* Risk management
* Portfolio allocation based on current regime
* Economic cycle analysis

## Licence

This project is licensed under the MIT Licence.
