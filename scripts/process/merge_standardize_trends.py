import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np
import glob
import os

from config import RAW_DATA_DIR, DATA_DIR

RAW_DIR = PROJECT_ROOT / RAW_DATA_DIR / "trends"
OUT_FILE = PROJECT_ROOT / DATA_DIR / "processed" / "trends_daily.csv"
OUT_LOG = PROJECT_ROOT / DATA_DIR / "processed" / "overlap_scaling_log.csv"


files = sorted(glob.glob(f"{RAW_DIR}/*.csv"))

merged = None 
logs = []

for i, f in enumerate(files):
    df = pd.read_csv(f, index_col=0, parse_dates=True)
    df.columns = ["trend"]

    if merged is None:
        merged = df.copy()
        continue

    overlap = merged.index.intersection(df.index)

    scale = 1.0

    if len(overlap) > 0:
        a = merged.loc[overlap, "trend"]
        b = df.loc[overlap, "trend"]

        valid = (a > 0) & (b > 0)
        ratios = (a[valid] / b[valid]).dropna()

        if len(ratios) > 0:
            scale = ratios.median()
            df["trend"] *= scale

        logs.append({
            "window_index": i,
            "file": os.path.basename(f),
            "overlap_days": len(overlap),
            "valid_ratios": len(ratios),
            "median_ratio": scale,
            "ratio_min": ratios.min() if len(ratios) > 0 else np.nan,
            "ratio_max": ratios.max() if len(ratios) > 0 else np.nan,
            "ratio_std": ratios.std() if len(ratios) > 1 else np.nan
        })

    merged = pd.concat([merged, df[~df.index.isin(merged.index)]])

merged = merged.sort_index()
merged.to_csv(OUT_FILE)

pd.DataFrame(logs).to_csv(OUT_LOG, index=False)

print(f"Trends merged and saved to {OUT_FILE}")
print(f"Overlap diagnostics saved to {OUT_LOG}")