import requests
import pandas as pd
from datetime import datetime

# Edit this list to your coverage universe (ISO3 codes per World Bank).
# Note: World Bank does not publish Taiwan (TWN). Hong Kong is HKG.
COUNTRY_CODES = [
    "USA","CHN","JPN","IND","HKG","CAN","FRA","GBR","SAU","DEU","CHE","AUS","KOR",
    "NLD","ESP","SWE","ARE","ZAF","IDN","ITA","BRA","BEL","SGP","DNK","THA","MEX",
    "MYS","TUR","NOR","ISR","PHL","FIN","POL","QAT","KWT","NZL","PRT","GRC",
    # add more as needed...
]

INDICATOR = "CM.MKT.LCAP.GD.ZS"
BASE_URL = "https://api.worldbank.org/v2"

def fetch_country_series(iso3: str) -> pd.DataFrame:
    # grab lots of rows to cover history; returns JSON with [metadata, data]
    url = f"{BASE_URL}/country/{iso3}/indicator/{INDICATOR}?format=json&per_page=2000"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    payload = r.json()
    if not isinstance(payload, list) or len(payload) < 2:
        return pd.DataFrame(columns=["country","countryiso3code","date","value"])
    rows = payload[1] or []
    df = pd.DataFrame(rows)[["country","countryiso3code","date","value"]]
    # unpack 'country' objects into names
    df["country"] = df["country"].apply(lambda x: x.get("value") if isinstance(x, dict) else x)
    # coerce types
    df["date"] = pd.to_numeric(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    # sort by most recent year first
    df = df.sort_values(["date"], ascending=False).reset_index(drop=True)
    return df

def latest_value(df: pd.DataFrame) -> pd.Series:
    # pick first non-null value (= latest year)
    row = df.dropna(subset=["value"]).head(1)
    if row.empty:
        return pd.Series({"Country": None, "Code": None, "Year": None, "PercentOfGDP": None, "BuffettIndicator": None})
    row = row.iloc[0]
    return pd.Series({
        "Country": row["country"],
        "Code": row["countryiso3code"],
        "Year": int(row["date"]),
        "PercentOfGDP": float(row["value"]),                  # already % of GDP
        "BuffettIndicator": float(row["value"]) / 100.0      # convert to ratio (e.g., 1.56 = 156%)
    })

results = []
for code in COUNTRY_CODES:
    try:
        df = fetch_country_series(code)
        results.append(latest_value(df))
    except Exception as e:
        results.append(pd.Series({"Country": None, "Code": code, "Year": None, "PercentOfGDP": None, "BuffettIndicator": None}))

out = pd.DataFrame(results)
out = out.dropna(subset=["PercentOfGDP"]).sort_values("BuffettIndicator", ascending=False).reset_index(drop=True)

print(out.to_string(index=False))

# Save CSV with a date-stamped filename
stamp = datetime.utcnow().strftime("%Y-%m-%d")
out.to_csv(f"buffett_indicator_latest_{stamp}.csv", index=False)
