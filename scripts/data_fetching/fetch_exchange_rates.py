import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import requests
import json
from urllib.parse import urlencode
import pandas as pd
from config import RAW_DATA_DIR, EVDS_API_KEY


OUT_FILE = PROJECT_ROOT / Path(RAW_DATA_DIR) / "usd_tl.csv"
api_key = EVDS_API_KEY

series_code='TP.DK.USD.S' # USD/TRY Döviz Kuru
start_date='01-01-1999'
end_date='31-12-2025'
frequency='1' # Günlük
aggregationType='avg'

params = {
    'series': series_code,
    'startDate': start_date,
    'endDate': end_date,
    'frequency': frequency,
    'aggregationTypes': aggregationType,
    'type': 'json'
}

url = f'https://evds2.tcmb.gov.tr/service/evds/{urlencode(params)}'

response = requests.get(url=url, headers={'key': api_key})
formatted_response = json.loads(response.content)

data = formatted_response['items']
df = pd.DataFrame(data)

df = df[["Tarih", "TP_DK_USD_S"]]
df = df.rename(columns={"Tarih": "Date", "TP_DK_USD_S": "USD_TL"})

df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors='coerce')
df["USD_TL"] = pd.to_numeric(df["USD_TL"], errors='coerce')

df.to_csv(OUT_FILE, index=False)