# Buffett-Indicator-by-country

Buffett Indicator by country (latest) via World Bank API
- Indicator: CM.MKT.LCAP.GD.ZS  (market cap of listed domestic companies as % of GDP)
- Output: dataframe + CSV with country, code, year, value (%), and a 'BuffettIndicator' ratio

Rough Valuation Guide (used by Buffett and analysts)
Buffett Indicator (% of GDP)	Market Valuation	Typical Long-Term Expectation
< 50%	Very Undervalued	High potential long-term gains (10–15%/yr possible)
50–75%	Undervalued / Fair	Solid long-term returns (7–10%/yr)
75–100%	Fair Value	Average long-term returns (~6–8%/yr)
100–150%	Moderately Overvalued	Lower expected gains (3–6%/yr)
>150%	Overvalued / Risky	Expect muted or volatile returns (0–3%/yr, sometimes negative)
