import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from pytrends.request import TrendReq
from datetime import datetime, timedelta
import time
import os

from config import LOGS_DIR, RAW_DATA_DIR

KEYWORD = "fındık fiyatı"
GEO = "TR"
START_DATE = datetime(2005, 1, 1)
END_DATE = datetime(2025, 12, 31)

WINDOW_DAYS = 90
OVERLAP_DAYS = 10

RAW_DIR = PROJECT_ROOT / Path(RAW_DATA_DIR) / "trends"
LOG_DIR = PROJECT_ROOT / Path(LOGS_DIR) / "trends.log"
os.makedirs(RAW_DIR, exist_ok=True)

pytrends = TrendReq(
    hl="tr-TR",
    tz=180,          # Türkiye timezone
    retries=3,
    backoff_factor=0.5
)

current_start = START_DATE

while current_start < END_DATE:
    current_end = min(current_start + timedelta(days=WINDOW_DAYS), END_DATE)

    timeframe = current_start.strftime("%Y-%m-%d") + " " + current_end.strftime("%Y-%m-%d")

    print(f"Fetching: {timeframe}")
    try:
        pytrends.build_payload(
            kw_list=[KEYWORD],
            geo=GEO,
            timeframe=timeframe
        )

        df = pytrends.interest_over_time()
    except Exception as e:
        print(e)
        time.sleep(15)

    if df.empty:
        with open(LOG_DIR, "a") as f:
            f.write(f"{timeframe}")
        print("Empty result, skipping!!")
    else:
        
        df = df.drop(columns=["isPartial"], errors="ignore")

        filename = (
            f"{KEYWORD.replace(' ', '_')}_"
            f"{current_start.strftime('%Y%m%d')}_"
            f"{current_end.strftime('%Y%m%d')}.csv"
        )

        df.to_csv(os.path.join(RAW_DIR, filename))

    current_start += timedelta(days=WINDOW_DAYS - OVERLAP_DAYS)

    time.sleep(5)
