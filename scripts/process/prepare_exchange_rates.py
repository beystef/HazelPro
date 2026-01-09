import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from config import DATA_DIR, RAW_DATA_DIR


currency_file = PROJECT_ROOT / Path(RAW_DATA_DIR) / "usd_tl.csv"
out_file = PROJECT_ROOT / Path(DATA_DIR) / "processed" / "usd_tl.csv"

df = pd.read_csv(currency_file, parse_dates=["Date"])
df = df.sort_values("Date").set_index("Date")
df.rename(columns={"USD_TL_Exchange_Rate": "USD_TL"}, inplace=True)

# standardize the currency
cutoff = pd.Timestamp('2005-01-01')
df.loc[df.index < cutoff, 'USD_TL'] /= 1_000_000

full_range = pd.date_range(df.index.min(), df.index.max(), freq="D")
df = df.reindex(full_range)

df["USD_TL"] = df["USD_TL"].interpolate(method="time")
df["USD_TL"] = df["USD_TL"].ffill().bfill()

df = df.reset_index().rename(columns={"index": "Date"})

out_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_file, index=False)