from dotenv import load_dotenv
import os

load_dotenv()

LOGS_DIR = "logs/"
DATA_DIR = "data/"
DATASETS_DIR = DATA_DIR + "datasets/"
RAW_DATA_DIR = DATA_DIR + "raw/"

FIG_DIR = "figures/"

EVDS_API_KEY = os.getenv("EVDS_API_KEY", None)

LAT = "40.9852301"
LON = "37.8797732"
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"