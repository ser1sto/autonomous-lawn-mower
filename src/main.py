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
TOMMOROWAPI_KEY = os.getenv("TOMMOROWAPI_KEY")
CSV_FILE_PATH = "/app/data/weather_log.csv"
# ===========================================================

def check_open_meteo():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=precipitation,precipitation_probability"
    print("\n--- 1. OPEN-METEO (Raw JSON) ---")
    try:
        res = requests.get(url, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(f"Current Precipitation: {res.json().get('current', {}).get('precipitation')} mm")
        print(f"Current Precipitation Probability: {res.json().get('current', {}).get('precipitation_probability')} %")
    except Exception as e:
        print(f"Błąd Open-Meteo: {e}")

def check_weather_api():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={WEATHERAPI_KEY}"
    print("\n--- 2. WEATHERAPI.COM (Raw JSON) ---")
    if not WEATHERAPI_KEY:
        print("Brak klucza WEATHERAPI_KEY w zmiennych środowiskowych!")
        return
    try:
        res = requests.get(url, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(f"Current Weather: {res.json()['weather'][0]['main']}")
    except Exception as e:
        print(f"Błąd WeatherAPI: {e}")

def check_tommorow_api():
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={LATITUDE},{LONGITUDE}&apikey={TOMMOROWAPI_KEY}"
    if not TOMMOROWAPI_KEY:
        print("Brak klucza TOMMOROWAPI_KEY w zmiennych środowiskowych!")
        return
    try:
        res = requests.get(url, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(f"Current Weather: {res.json()['data']['values']}")
    except Exception as e:
        print(f"Błąd TommorowAPI: {e}")



if __name__ == "__main__":
    print(f"Sprawdzanie API dla lokalizacji: {LATITUDE}, {LONGITUDE}")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    check_open_meteo()
    check_weather_api()
    check_tommorow_api()