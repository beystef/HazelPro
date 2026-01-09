import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import glob
import os

from config import RAW_DATA_DIR, LOGS_DIR, DATA_DIR

WEATHER_DIR = PROJECT_ROOT / RAW_DATA_DIR / "weather"
OUT_FILE = PROJECT_ROOT / DATA_DIR / "processed" / "weather_daily_1999_2025.csv"
LOG_FILE = os.path.join(LOGS_DIR, "weather_merge.log")

EXPECTED_COLUMNS = [
    "date",
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "precipitation_sum",
    "rain_sum",
    "wind_speed_10m_max",
    "et0_fao_evapotranspiration"
]

def main():
    files = sorted(glob.glob(os.path.join(WEATHER_DIR, "weather-data-*.csv")))

    if not files:
        print("No files exist, check raw data!!")
        return

    dfs = []
    for f in files:
        df = pd.read_csv(f, parse_dates=["date"])

        missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)

        if missing_cols:
            print(f"Missing columns in {f}: {missing_cols}, ---- filling with zeros, check the data!!")
            with open(LOG_FILE, "a") as f:
                f.write(f"Missing columns in {f}: {missing_cols}\n")
            for col in missing_cols:
                df[col] = 0

        dfs.append(df)

    weather = pd.concat(dfs, ignore_index=True)
    weather.sort_values("date", inplace=True)

    duplicates = weather[weather.duplicated("date")]
    if not duplicates.empty:
        duplicates.to_csv(LOG_FILE.replace(".log", "_duplicates.csv"), index=False)
        raise ValueError("Duplicate dates detected!")

    full_range = pd.date_range(weather["date"].min(), weather["date"].max(), freq="D")
    missing = full_range.difference(weather["date"])

    with open(LOG_FILE, "a") as f:
        f.write(f"Total days: {len(weather)}\n")
        f.write(f"Date range: {weather['date'].min()} → {weather['date'].max()}\n")
        f.write(f"Missing days: {len(missing)}\n")

    if len(missing) > 0:
        pd.DataFrame({"missing_date": missing}).to_csv(
            LOG_FILE.replace(".log", "_missing_days.csv"),
            index=False
        )

    weather.to_csv(OUT_FILE, index=False)
    print(f"Merged weather data saved to:\n{OUT_FILE}")

if __name__ == "__main__":
    main()