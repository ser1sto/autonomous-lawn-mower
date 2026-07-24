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
METEOSOURCEAPI_KEY = os.getenv("METEOSOURCEAPI_KEY")
CSV_FILE_PATH = "/app/data/weather_log.csv"
# ===========================================================

def check_open_meteo():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=precipitation,precipitation_probability"
    try:
        res = requests.get(url, timeout=5)
        print("\n--- 1. OPEN-METEO (Raw JSON) ---")
        print(f"Status Code: {res.status_code}")
        print(f"Current Precipitation: {res.json().get('current', {}).get('precipitation')} mm")
        print(f"Current Precipitation Probability: {res.json().get('current', {}).get('precipitation_probability')}")
    except Exception as e:
        print(f"Błąd Open-Meteo: {e}")

def check_weather_api():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={WEATHERAPI_KEY}"
    if not WEATHERAPI_KEY:
        print("Brak klucza WEATHERAPI_KEY w zmiennych środowiskowych!")
        return
    try:
        res = requests.get(url, timeout=5)
        print("\n--- 2. WEATHERAPI.COM (Raw JSON) ---")
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
        print("\n--- 3. TOMMOROWAPI.COM (Raw JSON) ---")
        print(f"Status Code: {res.status_code}")
        print(f"Current Precipitation: {res.json()['data']['values']['rainIntensity']} mm")
        print(f"Precipitation Probability: {res.json()['data']['values']['precipitationProbability']}")
    except Exception as e:
        print(f"Błąd TommorowAPI: {e}")

def check_meteosource_api():
    url = f"https://www.meteosource.com/api/v1/free/point?lat={LATITUDE}&lon={LONGITUDE}&sections=current&language=en&units=metric&key={METEOSOURCEAPI_KEY}"
    if not METEOSOURCEAPI_KEY:
        print("Brak klucza METEOSOURCEAPI_KEY w zmiennych środowiskowych!")
        return
    try:
        res = requests.get(url, timeout=5)
        print("\n--- 4. METEOSOURCEAPI.COM (Raw JSON) ---")
        print(f"Status Code: {res.status_code}")
        print(f"Current Precipitation: {res.json()['current']['precipitation']['total']} mm")
    except Exception as e:
        print(f"Błąd MeteosourceAPI: {e}")



if __name__ == "__main__":
    print(f"Sprawdzanie API dla lokalizacji: {LATITUDE}, {LONGITUDE}")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    check_open_meteo()
    check_weather_api()
    check_tommorow_api()
    check_meteosource_api()