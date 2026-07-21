import requests
import json
import os
import csv
from datetime import datetime
import time
from dotenv import load_dotenv


# Wczytanie zmiennych z pliku .env
load_dotenv()

# ================= CONFIGURATION FROM .ENV =================
LATITUDE = float(os.getenv("LATITUDE"))
LONGITUDE = float(os.getenv("LONGITUDE"))
NTFY_TOPIC = os.getenv("NTFY_TOPIC")
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES"))
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
CSV_FILE_PATH = "/app/data/weather_log.csv"
# ===========================================================

def check_open_meteo():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=precipitation,precipitation_probability"
    print("\n--- 1. OPEN-METEO (Raw JSON) ---")
    try:
        res = requests.get(url, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(json.dumps(res.json(), indent=4))
    except Exception as e:
        print(f"Błąd Open-Meteo: {e}")

def check_weather_api():
    print("\n--- 2. WEATHERAPI.COM (Raw JSON) ---")
    if not WEATHERAPI_KEY:
        print("Brak klucza WEATHERAPI_KEY w zmiennych środowiskowych!")
        return
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={WEATHERAPI_KEY}"
    
    try:
        res = requests.get(url, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(json.dumps(res.json(), indent=4))
    except Exception as e:
        print(f"Błąd WeatherAPI: {e}")

if __name__ == "__main__":
    print(f"Sprawdzanie API dla lokalizacji: {LATITUDE}, {LONGITUDE}")
    check_open_meteo()
    print('###############################################')
    check_weather_api()