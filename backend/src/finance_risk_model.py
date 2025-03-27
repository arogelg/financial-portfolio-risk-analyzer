# -*- coding: utf-8 -*-
"""finance_risk_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AnVO8vjg-4o3tJEG9F6DnzCPsht8QfM-
"""

"""
Financial Risk Analyzer for S&P 500 Companies
---------------------------------------------
This python script:
1. Retrieves the current S&P 500 tickers and their sectors from Wikipedia.
2. Fetches historical stock data using Yahoo Finance (via yfinance).
3. Calculates financial risk metrics (Volatility, VaR, Drawdown, Beta).
4. Assigns a composite risk level (Low / Moderate / High).
5. Outputs one CSV file per industry sector in /output/industries.

Author: Andres Alvarez
Date: 2025-03
"""

import os
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict
#finance_risk_model.py


# ====================================
# SECTION 1: Set functions to retrieve data and calculate risk model
# ====================================

# Function gets S&P 500 tickers with GICS Sector and Sub-Industry from Wikipedia.

def get_sp500_tickers_with_industry() -> pd.DataFrame:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]
    df['Symbol'] = df['Symbol'].str.replace('.', '-', regex=False)  # For Yahoo compatibility
    return df[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']]

#Ensures the ticker is compatible with Yahoo Finance.
def sanitize_ticker(ticker: str) -> str:
    return ticker.replace('.', '-')


# ====================================
# SECTION 2: Risk Analysis Functions
# ====================================


#Retrieves historical closing prices for a given stock.
def fetch_stock_data(ticker: str, period="1y", interval="1d") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist[['Close']].dropna()

#Compute daily returns from closing prices.
def calculate_daily_returns(prices: pd.Series) -> pd.Series:
    return prices.pct_change().dropna()

#Calculate the annualized volatility of daily returns.
def calculate_annualized_volatility(returns: pd.Series) -> float:
    return np.std(returns) * np.sqrt(252)

#Calculates historical Value at Risk (VaR) at 95% confidence level.
def calculate_var(returns: pd.Series, confidence_level=0.05) -> float:
    return np.percentile(returns, 100 * confidence_level)

#Calculate historical Value at Risk (VaR) at 95% confidence level.
def calculate_max_drawdown(prices: pd.Series) -> float:
    cumulative = prices.cummax()
    drawdown = (prices - cumulative) / cumulative
    return drawdown.min()


#Calculate beta vs. the market (SPY).
def calculate_beta(stock_returns: pd.Series, market_returns: pd.Series) -> float:
    cov = np.cov(stock_returns, market_returns)[0][1]
    market_var = np.var(market_returns)
    return cov / market_var if market_var != 0 else 0


#Assign a qualitative risk level based on financial risk metrics.
def composite_risk_score(vol: float, var: float, dd: float, beta: float) -> str:
    score = 0
    score += (vol > 0.03)
    score += (var < -0.03)
    score += (dd < -0.20)
    score += (beta > 1.2)

    if score >= 3:
        return "High Risk"
    elif score == 2:
        return "Moderate Risk"
    else:
        return "Low Risk"

#Run the full risk analysis pipeline for a given stock.
def analyze_stock(ticker: str, market_ticker: str = "SPY") -> Dict:
    try:
        stock_data = fetch_stock_data(ticker)
        market_data = fetch_stock_data(market_ticker)

        stock_returns = calculate_daily_returns(stock_data['Close'])
        market_returns = calculate_daily_returns(market_data['Close']).loc[stock_returns.index]

        vol = calculate_annualized_volatility(stock_returns)
        var = calculate_var(stock_returns)
        drawdown = calculate_max_drawdown(stock_data['Close'])
        beta = calculate_beta(stock_returns, market_returns)
        risk = composite_risk_score(vol, var, drawdown, beta)

        return {
            "Ticker": ticker,
            "Volatility": round(vol, 4),
            "VaR (95%)": round(var, 4),
            "Max Drawdown": round(drawdown, 4),
            "Beta vs SPY": round(beta, 4),
            "Risk Level": risk,
            "Latest Close": round(stock_data['Close'].iloc[-1], 2)
        }
    except Exception as e:
        return {"Ticker": ticker, "Error": str(e)}


# ====================================
# SECTION 3: Batch Processing by Industry
# ====================================

def run_analysis_by_industry():
    """
    Run analysis by industry and save:
    1. One CSV per industry
    2. One master CSV with all results
    """
    print("Fetching S&P 500 tickers and industry info...")
    df = get_sp500_tickers_with_industry()
    grouped = df.groupby("GICS Sector")

    output_dir = "output/industries"
    os.makedirs(output_dir, exist_ok=True)

    all_results = []  # Collect everything here for the master file

    for sector, group in grouped:
        print(f"\nAnalyzing sector: {sector}")
        sector_results = []

        for _, row in group.iterrows():
            ticker = row['Symbol']
            security = row['Security']
            sub_industry = row['GICS Sub-Industry']

            print(f"  ➜ {ticker}", end='')

            result = analyze_stock(ticker)

            if 'Error' in result:
                print(f"Skipped ({result['Error']})")
                continue

            # Add sector info for better context
            result['Sector'] = sector
            result['Company'] = security
            result['Sub-Industry'] = sub_industry

            sector_results.append(result)
            all_results.append(result)
            print("(check done)")

        # Save per-industry file
        if sector_results:
            filename = f"{output_dir}/{sector.replace('/', '_')}.csv"
            pd.DataFrame(sector_results).to_csv(filename, index=False)
            print(f"Saved {len(sector_results)} stocks to {filename}")
        else:
            print("No valid stocks analyzed for this sector.")

    # Save master file with all results
    if all_results:
        master_file = "output/all_sectors.csv"
        pd.DataFrame(all_results).to_csv(master_file, index=False)
        print(f"\nMaster file saved to: {master_file}")

# ====================================
# SECTION 4: Entry Point
# ====================================

if __name__ == "__main__":
    run_analysis_by_industry()
    print("\n All sectors processed. Results saved to 'output/industries/' folder.")

# ====================================
# SECTION 5: Download all csv files (ran to download files to local machine)
# ====================================
from google.colab import files
import shutil

# Zip the entire output folder
shutil.make_archive("portfolio_risk_analysis", 'zip', "output")

# Download the zip file
files.download("portfolio_risk_analysis.zip")