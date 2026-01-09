import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
import pandas as pd
from config import DATA_DIR, RAW_DATA_DIR

otb_raw_data_dir = PROJECT_ROOT / RAW_DATA_DIR / "OTB"
data_file_path = otb_raw_data_dir / "OTB Günlük Fiyat 1999-2025 - Merged.xlsx"
OUT_FILE = PROJECT_ROOT / DATA_DIR / "raw" / "hazelnut_price.csv"
OUT_INTERP = PROJECT_ROOT / DATA_DIR / "processed" / "hazelnut_price.csv"
CURRENCY_FILE = PROJECT_ROOT / DATA_DIR / "processed" / "usd_tl.csv"

turkish_months = {
    "OCAK": 1, "ŞUBAT": 2, "MART": 3, "NİSAN": 4, "MAYIS": 5, "HAZİRAN": 6,
    "TEMMUZ": 7, "AĞUSTOS": 8, "EYLÜL": 9, "EKİM": 10, "KASIM": 11, "ARALIK": 12
}

dfs = pd.read_excel(data_file_path, sheet_name=None, header=2)
all_data = []

for year, df in dfs.items():
    df = df.set_index(df.columns[0])
    df.index.name = "Day"
    df = df.dropna(how="all")
    temp = df.stack().reset_index()
    temp.columns = ["Day", "Month_TR", "Value"]
    temp["Month_TR_clean"] = temp["Month_TR"].astype(str).str.strip().str.upper()
    temp["Month"] = temp["Month_TR_clean"].map(turkish_months)
    temp = temp.dropna(subset=["Month"])
    temp["Date"] = pd.to_datetime(
        temp["Day"].astype(int).astype(str) + "-" +
        temp["Month"].astype(int).astype(str) + "-" +
        str(year),
        format="%d-%m-%Y",
        errors="coerce"
    )
    temp = temp.dropna(subset=["Date"])
    all_data.append(temp[["Date", "Value"]])

ts = pd.concat(all_data, ignore_index=True)
ts = ts.sort_values("Date").reset_index(drop=True)
ts["Value"] = pd.to_numeric(ts["Value"].astype(str).str.strip()
                            .str.replace("--", "").str.replace("*", "")
                            .str.replace(",", "."), errors="coerce")


ts.to_csv(OUT_FILE, index=False)
print(f"Saved merge data to {OUT_FILE}")

# standardize the prices
cutoff = pd.Timestamp('2005-01-01')
ts.loc[ts['Date'] < cutoff, 'Value'] /= 1_000_000

dfi = ts.set_index("Date").asfreq("D")
dfi["iValue"] = (
    dfi["Value"]
    .interpolate(method="linear", limit=7, limit_direction="both")
)
dfi["rolling_14d"] = dfi["iValue"].rolling(window=14, min_periods=1).mean()

currency_df = pd.read_csv(CURRENCY_FILE, parse_dates=["Date"])
currency_df = currency_df.set_index("Date")

dfi = dfi.join(currency_df[["USD_TL"]], how="left")

dfi["AdjustedValue"] = dfi["Value"] / dfi["USD_TL"]
dfi["iAdjusted"] = dfi["iValue"] / dfi["USD_TL"]
dfi["rolling_14d_adjusted"] = dfi["rolling_14d"] / dfi["USD_TL"]

dfi_reset = dfi.reset_index()
dfi_reset = dfi_reset[["Date", "Value", "iValue", "rolling_14d", 
                        "AdjustedValue", "iAdjusted", "rolling_14d_adjusted", "USD_TL"]]

dfi_reset.to_csv(OUT_INTERP, index=False)
print(f"Saved interpolated data (7-day limit) with 14-day rolling and USD-adjusted prices to {OUT_INTERP}")