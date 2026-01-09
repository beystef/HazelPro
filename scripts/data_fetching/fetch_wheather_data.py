import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import requests
import pandas as pd
import time
from datetime import datetime, timedelta

from config import LAT, LON, BASE_URL, RAW_DATA_DIR, LOGS_DIR

LOG_FILE_PATH = PROJECT_ROOT / LOGS_DIR / "weather.logs"

CHUNK_DAYS = 7

DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "precipitation_sum",
    "rain_sum",
    "wind_speed_10m_max",
    "et0_fao_evapotranspiration"
]

def get_chunks(start, end, chunk_days=7):
    chunks = []
    current = start
    while current <= end:
        chunk_end = min(current + timedelta(days=chunk_days - 1), end)
        chunks.append([current, chunk_end])
        current = chunk_end + timedelta(days=1)
    return chunks

def fetch_chunk(start_date, end_date):
    print("fetching", start_date, end_date, end="   ")
    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "daily": DAILY_VARS,
        "timezone": "GMT"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        with open(LOG_FILE_PATH, "a") as f:
            f.write(f"{start_date}-{end_date}")
            print("ERROR!!")
        return {}
    print("DONE!")
    return response.json()

def collect_weather(year, startdate, enddate):
    OUT_FILE_PATH = PROJECT_ROOT / RAW_DATA_DIR / "weather" / f"weather-data-{year}.csv"
    print(f"Starting data collection for {startdate}:{enddate}")

    start = datetime.fromisoformat(startdate)
    end = datetime.fromisoformat(enddate)

    all_days = []
    chunks = get_chunks(start, end, CHUNK_DAYS)

    for chunk_start, chunk_end in chunks:
        data = fetch_chunk(chunk_start, chunk_end)
        daily = data.get("daily", {})

        df = pd.DataFrame(daily)
        df.rename(columns={"time": "date"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"])

        all_days.append(df)
        time.sleep(1)

    weather_df = pd.concat(all_days, ignore_index=True)
    weather_df.sort_values("date", inplace=True)

    weather_df.to_csv(OUT_FILE_PATH, index=False)
    print(f"Weather data saved to: {OUT_FILE_PATH}")

if __name__ == "__main__":
    start_year = 1999
    end_year = 2025
    for year in range(start_year, end_year+1):
        START_DATE = f"{year}-01-01"
        END_DATE = f"{year}-12-31"
        collect_weather(year, START_DATE, END_DATE)
