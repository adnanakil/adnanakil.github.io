#!/usr/bin/env python3
"""
Simple script to calculate effective corporate tax rates using FRED data.

Key FRED Series Used:
- B075RC1Q027SBEA: Federal government current tax receipts: Taxes on corporate income (Quarterly)
- A053RC1Q027SBEA: Corporate profits before tax (without IVA and CCAdj) (Quarterly)
- FCTAX: Federal Government: Tax Receipts on Corporate Income (Annual)

Effective Tax Rate = (Corporate Tax Receipts / Corporate Profits Before Tax) × 100
"""

import pandas as pd
import requests

def fetch_fred_series(series_id, api_key, start_date='1950-01-01'):
    """
    Fetch data from FRED API.
    
    Parameters:
    -----------
    series_id : str
        FRED series ID
    api_key : str
        Your FRED API key
    start_date : str
        Start date in 'YYYY-MM-DD' format
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with date as index and value column
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'sort_order': 'asc'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Convert to DataFrame
    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df[['date', 'value']].dropna()
    df.set_index('date', inplace=True)
    
    return df

def calculate_effective_rate(tax_receipts, profits_before_tax):
    """Calculate effective tax rate as percentage."""
    # Align series by date
    combined = pd.concat([tax_receipts, profits_before_tax], axis=1, join='inner')
    combined.columns = ['taxes', 'profits']
    
    # Calculate rate
    effective_rate = (combined['taxes'] / combined['profits']) * 100
    
    return effective_rate

def main():
    # Example usage
    api_key = 'YOUR_API_KEY_HERE'  # Replace with your FRED API key
    
    # Key series IDs
    TAX_RECEIPTS_QUARTERLY = 'B075RC1Q027SBEA'
    PROFITS_BEFORE_TAX_QUARTERLY = 'A053RC1Q027SBEA'
    TAX_RECEIPTS_ANNUAL = 'FCTAX'
    
    print("Effective Corporate Tax Rate Calculator")
    print("="*50)
    print("\nKey FRED Series:")
    print(f"- Tax Receipts (Quarterly): {TAX_RECEIPTS_QUARTERLY}")
    print(f"- Profits Before Tax (Quarterly): {PROFITS_BEFORE_TAX_QUARTERLY}")
    print(f"- Tax Receipts (Annual): {TAX_RECEIPTS_ANNUAL}")
    print("\nFormula: Effective Tax Rate = (Tax Receipts / Profits Before Tax) × 100")
    
    # Example calculation (uncomment with your API key)
    """
    # Fetch quarterly data
    tax_receipts = fetch_fred_series(TAX_RECEIPTS_QUARTERLY, api_key)
    profits = fetch_fred_series(PROFITS_BEFORE_TAX_QUARTERLY, api_key)
    
    # Calculate effective rate
    effective_rate = calculate_effective_rate(tax_receipts['value'], profits['value'])
    
    # Display recent rates
    print(f"\nRecent Quarterly Effective Corporate Tax Rates:")
    print(effective_rate.tail(8))
    
    # Annual average
    annual_rate = effective_rate.resample('A').mean()
    print(f"\nRecent Annual Average Effective Tax Rates:")
    print(annual_rate.tail(5))
    """

if __name__ == "__main__":
    main()