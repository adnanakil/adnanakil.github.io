# Corporate Tax Data Sources Reference

## FRED (Federal Reserve Economic Data) Series

### Primary Series for Calculating Effective Corporate Tax Rates

#### Tax Receipt Series
1. **FCTAX** - Federal Government: Tax Receipts on Corporate Income
   - Frequency: Annual
   - Start Date: 1929
   - URL: https://fred.stlouisfed.org/series/FCTAX

2. **B075RC1Q027SBEA** - Federal government current tax receipts: Taxes on corporate income
   - Frequency: Quarterly
   - Start Date: Q1 1947
   - URL: https://fred.stlouisfed.org/series/B075RC1Q027SBEA

#### Corporate Profits Series
1. **A053RC1Q027SBEA** - National income: Corporate profits before tax (without IVA and CCAdj)
   - Frequency: Quarterly
   - Start Date: Q1 1947
   - URL: https://fred.stlouisfed.org/series/A053RC1Q027SBEA

2. **CP** - Corporate Profits After Tax (without IVA and CCAdj)
   - Frequency: Quarterly
   - Start Date: Q1 1947
   - URL: https://fred.stlouisfed.org/series/CP

3. **CPROFIT** - Corporate Profits with IVA and CCAdj
   - Frequency: Quarterly
   - Start Date: Q1 1947
   - URL: https://fred.stlouisfed.org/series/CPROFIT

### Calculating Effective Corporate Tax Rate

**Formula**: Effective Tax Rate = (Corporate Tax Receipts / Corporate Profits Before Tax) × 100

**Using FRED Data**:
- Quarterly: Use B075RC1Q027SBEA / A053RC1Q027SBEA
- Annual: Use FCTAX / (Annual sum of A053RC1Q027SBEA)

## Other Official Data Sources

### Congressional Budget Office (CBO)
- **Historical Effective Tax Rates**: https://www.cbo.gov/topics/taxes/tax-rates
- **Corporate Tax Analysis**: https://www.cbo.gov/publication/59149
- Provides analysis of effective tax rates from 1979 onwards
- Includes international comparisons and policy analysis

### Bureau of Economic Analysis (BEA)
- **National Income and Product Accounts (NIPA)**: https://www.bea.gov/data/income-saving/corporate-profits
- Source for corporate profits data used in FRED
- Provides detailed breakdowns of corporate income and taxes

### Tax Policy Center
- **Corporate Tax Statistics**: https://www.taxpolicycenter.org/statistics
- Historical statutory and effective tax rate comparisons
- Policy analysis and revenue estimates

## Key Considerations

1. **IVA and CCAdj**: 
   - IVA = Inventory Valuation Adjustment
   - CCAdj = Capital Consumption Adjustment
   - Series without these adjustments provide cleaner comparisons for tax rate calculations

2. **Historical Data Availability**:
   - Annual data: Available from 1929 (FCTAX series)
   - Quarterly data: Available from 1947 (most series)
   - Most comprehensive data: Post-1950

3. **Effective vs. Statutory Rates**:
   - Effective rates show actual taxes paid relative to profits
   - Statutory rates are the legal tax rates set by law
   - Gap between them reflects deductions, credits, and tax planning

4. **Recent Changes**:
   - 2017 Tax Cuts and Jobs Act reduced corporate rate from 35% to 21%
   - Important to note structural breaks in the data around major tax reforms

## API Access

### FRED API
- Register for free API key: https://fred.stlouisfed.org/docs/api/api_key.html
- API Documentation: https://fred.stlouisfed.org/docs/api/fred/
- Rate limits: 120 requests per minute

### Example API Call
```
https://api.stlouisfed.org/fred/series/observations?series_id=B075RC1Q027SBEA&api_key=YOUR_KEY&file_type=json
```

## Python Libraries for Data Access
- `fredapi`: Official Python interface to FRED
- `pandas-datareader`: Supports FRED data access
- `requests`: For direct API calls

## Additional Context

### Why Effective Tax Rates Matter
- Show actual tax burden on corporations
- Differ from statutory rates due to deductions and credits
- Important for policy analysis and international comparisons
- Reveal impact of tax reforms over time

### Methodological Notes
- Use consistent series (with or without adjustments)
- Consider seasonal adjustments for quarterly data
- Be aware of revisions in historical data
- Account for changes in tax law when analyzing trends