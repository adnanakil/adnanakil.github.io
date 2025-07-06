#!/usr/bin/env python3
"""
Fetch effective corporate tax rate data from FRED (Federal Reserve Economic Data).

This script calculates effective corporate tax rates by dividing actual corporate tax receipts
by corporate profits before tax. It fetches data from multiple FRED series to provide
comprehensive historical analysis.
"""

import pandas as pd
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class CorporateTaxDataFetcher:
    def __init__(self, api_key=None):
        """
        Initialize the FRED data fetcher.
        
        Parameters:
        -----------
        api_key : str
            FRED API key. If not provided, you'll need to set it manually.
            Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
        """
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        
        # Key FRED series for corporate tax analysis
        self.series_info = {
            # Tax Receipt Series
            'FCTAX': {
                'name': 'Federal Government: Tax Receipts on Corporate Income',
                'frequency': 'Annual',
                'start_date': '1929-01-01'
            },
            'B075RC1Q027SBEA': {
                'name': 'Federal government current tax receipts: Taxes on corporate income',
                'frequency': 'Quarterly',
                'start_date': '1947-01-01'
            },
            
            # Corporate Profits Series
            'A053RC1Q027SBEA': {
                'name': 'Corporate profits before tax (without IVA and CCAdj)',
                'frequency': 'Quarterly',
                'start_date': '1947-01-01'
            },
            'CP': {
                'name': 'Corporate Profits After Tax (without IVA and CCAdj)',
                'frequency': 'Quarterly',
                'start_date': '1947-01-01'
            },
            
            # Additional Context Series
            'CPROFIT': {
                'name': 'Corporate Profits with IVA and CCAdj',
                'frequency': 'Quarterly',
                'start_date': '1947-01-01'
            }
        }
    
    def fetch_series(self, series_id, start_date=None, end_date=None):
        """
        Fetch a specific FRED series.
        
        Parameters:
        -----------
        series_id : str
            FRED series ID
        start_date : str
            Start date in 'YYYY-MM-DD' format
        end_date : str
            End date in 'YYYY-MM-DD' format
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with date and value columns
        """
        if not self.api_key:
            raise ValueError("API key not set. Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html")
        
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'sort_order': 'asc'
        }
        
        if start_date:
            params['observation_start'] = start_date
        if end_date:
            params['observation_end'] = end_date
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Convert to DataFrame
            observations = data['observations']
            df = pd.DataFrame(observations)
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df[['date', 'value']].dropna()
            df.set_index('date', inplace=True)
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {series_id}: {e}")
            return pd.DataFrame()
    
    def calculate_effective_tax_rate(self, tax_receipts, profits_before_tax):
        """
        Calculate effective corporate tax rate.
        
        Parameters:
        -----------
        tax_receipts : pd.Series
            Corporate tax receipts
        profits_before_tax : pd.Series
            Corporate profits before tax
            
        Returns:
        --------
        pd.Series
            Effective tax rate (as percentage)
        """
        # Align the series by date
        aligned = pd.concat([tax_receipts, profits_before_tax], axis=1, join='inner')
        aligned.columns = ['tax_receipts', 'profits_before_tax']
        
        # Calculate effective tax rate
        effective_rate = (aligned['tax_receipts'] / aligned['profits_before_tax']) * 100
        
        return effective_rate
    
    def fetch_all_corporate_tax_data(self, start_date='1950-01-01'):
        """
        Fetch all relevant corporate tax data and calculate effective tax rates.
        
        Parameters:
        -----------
        start_date : str
            Start date for data retrieval
            
        Returns:
        --------
        dict
            Dictionary containing all fetched data and calculated rates
        """
        results = {}
        
        print("Fetching corporate tax data from FRED...")
        
        # Fetch quarterly data
        print("\nFetching quarterly data:")
        
        # Tax receipts (quarterly)
        print("- Federal tax receipts on corporate income...")
        tax_receipts_q = self.fetch_series('B075RC1Q027SBEA', start_date=start_date)
        results['tax_receipts_quarterly'] = tax_receipts_q
        
        # Profits before tax (quarterly)
        print("- Corporate profits before tax...")
        profits_before_tax_q = self.fetch_series('A053RC1Q027SBEA', start_date=start_date)
        results['profits_before_tax_quarterly'] = profits_before_tax_q
        
        # Profits after tax (quarterly)
        print("- Corporate profits after tax...")
        profits_after_tax_q = self.fetch_series('CP', start_date=start_date)
        results['profits_after_tax_quarterly'] = profits_after_tax_q
        
        # Calculate quarterly effective tax rate
        if not tax_receipts_q.empty and not profits_before_tax_q.empty:
            print("\nCalculating quarterly effective tax rate...")
            effective_rate_q = self.calculate_effective_tax_rate(
                tax_receipts_q['value'],
                profits_before_tax_q['value']
            )
            results['effective_tax_rate_quarterly'] = effective_rate_q
        
        # Fetch annual data
        print("\nFetching annual data:")
        
        # Tax receipts (annual)
        print("- Federal tax receipts on corporate income (annual)...")
        tax_receipts_a = self.fetch_series('FCTAX', start_date=start_date)
        results['tax_receipts_annual'] = tax_receipts_a
        
        # Convert quarterly to annual for comparison
        if not profits_before_tax_q.empty:
            print("\nConverting quarterly data to annual...")
            profits_before_tax_a = profits_before_tax_q.resample('A').sum()
            tax_receipts_q_annual = tax_receipts_q.resample('A').sum()
            
            # Calculate annual effective tax rate from quarterly data
            effective_rate_a = self.calculate_effective_tax_rate(
                tax_receipts_q_annual['value'],
                profits_before_tax_a['value']
            )
            results['effective_tax_rate_annual'] = effective_rate_a
        
        return results
    
    def plot_effective_tax_rates(self, data_dict, save_path=None):
        """
        Plot effective corporate tax rates over time.
        
        Parameters:
        -----------
        data_dict : dict
            Dictionary containing the data to plot
        save_path : str
            Path to save the plot (optional)
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot quarterly effective tax rate
        if 'effective_tax_rate_quarterly' in data_dict:
            rate_q = data_dict['effective_tax_rate_quarterly']
            ax1.plot(rate_q.index, rate_q.values, 'b-', linewidth=1.5, label='Quarterly')
            
            # Add moving average
            ma = rate_q.rolling(window=4).mean()
            ax1.plot(ma.index, ma.values, 'r-', linewidth=2, label='4-Quarter MA')
            
            ax1.set_title('Effective Corporate Tax Rate (Quarterly)', fontsize=14)
            ax1.set_ylabel('Effective Tax Rate (%)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.legend()
        
        # Plot annual effective tax rate
        if 'effective_tax_rate_annual' in data_dict:
            rate_a = data_dict['effective_tax_rate_annual']
            ax2.plot(rate_a.index, rate_a.values, 'g-', linewidth=2, marker='o', markersize=4)
            
            # Add trend line
            x = np.arange(len(rate_a))
            z = np.polyfit(x, rate_a.values, 1)
            p = np.poly1d(z)
            ax2.plot(rate_a.index, p(x), 'r--', alpha=0.8, label=f'Trend: {z[0]:.2f}% per year')
            
            ax2.set_title('Effective Corporate Tax Rate (Annual)', fontsize=14)
            ax2.set_ylabel('Effective Tax Rate (%)', fontsize=12)
            ax2.set_xlabel('Year', fontsize=12)
            ax2.grid(True, alpha=0.3)
            ax2.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nPlot saved to: {save_path}")
        
        plt.show()
    
    def export_to_csv(self, data_dict, prefix='corporate_tax_data'):
        """
        Export data to CSV files.
        
        Parameters:
        -----------
        data_dict : dict
            Dictionary containing the data to export
        prefix : str
            Prefix for output filenames
        """
        for key, data in data_dict.items():
            if isinstance(data, (pd.DataFrame, pd.Series)):
                filename = f"{prefix}_{key}.csv"
                data.to_csv(filename)
                print(f"Exported {key} to {filename}")
    
    def summary_statistics(self, data_dict):
        """
        Calculate and display summary statistics for effective tax rates.
        
        Parameters:
        -----------
        data_dict : dict
            Dictionary containing the data
        """
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        if 'effective_tax_rate_quarterly' in data_dict:
            rate_q = data_dict['effective_tax_rate_quarterly']
            print(f"\nQuarterly Effective Tax Rate ({rate_q.index[0].year}-{rate_q.index[-1].year}):")
            print(f"  Mean:     {rate_q.mean():.2f}%")
            print(f"  Median:   {rate_q.median():.2f}%")
            print(f"  Std Dev:  {rate_q.std():.2f}%")
            print(f"  Min:      {rate_q.min():.2f}% ({rate_q.idxmin().strftime('%Y-%m')})")
            print(f"  Max:      {rate_q.max():.2f}% ({rate_q.idxmax().strftime('%Y-%m')})")
            
            # Decade averages
            print("\nDecade Averages:")
            for decade in range(1950, 2030, 10):
                decade_data = rate_q[(rate_q.index.year >= decade) & (rate_q.index.year < decade + 10)]
                if not decade_data.empty:
                    print(f"  {decade}s: {decade_data.mean():.2f}%")
        
        if 'effective_tax_rate_annual' in data_dict:
            rate_a = data_dict['effective_tax_rate_annual']
            print(f"\nAnnual Effective Tax Rate ({rate_a.index[0].year}-{rate_a.index[-1].year}):")
            print(f"  Mean:     {rate_a.mean():.2f}%")
            print(f"  Median:   {rate_a.median():.2f}%")
            print(f"  Std Dev:  {rate_a.std():.2f}%")
            print(f"  Min:      {rate_a.min():.2f}% ({rate_a.idxmin().year})")
            print(f"  Max:      {rate_a.max():.2f}% ({rate_a.idxmax().year})")


def main():
    """
    Main function to demonstrate usage.
    """
    # Initialize fetcher (you'll need to provide your API key)
    # Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
    
    print("Corporate Tax Data Fetcher")
    print("="*60)
    print("\nTo use this script, you'll need a FRED API key.")
    print("Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html")
    print("\nExample usage:")
    print("  fetcher = CorporateTaxDataFetcher(api_key='your_api_key_here')")
    print("  data = fetcher.fetch_all_corporate_tax_data(start_date='1950-01-01')")
    print("  fetcher.summary_statistics(data)")
    print("  fetcher.plot_effective_tax_rates(data)")
    
    # Example with API key (uncomment and add your key)
    # api_key = 'YOUR_API_KEY_HERE'
    # fetcher = CorporateTaxDataFetcher(api_key=api_key)
    # 
    # # Fetch all data
    # data = fetcher.fetch_all_corporate_tax_data(start_date='1950-01-01')
    # 
    # # Display summary statistics
    # fetcher.summary_statistics(data)
    # 
    # # Plot the results
    # fetcher.plot_effective_tax_rates(data, save_path='effective_corporate_tax_rates.png')
    # 
    # # Export to CSV
    # fetcher.export_to_csv(data)


if __name__ == "__main__":
    main()