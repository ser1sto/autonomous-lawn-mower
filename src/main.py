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
LATITUDE = float(os.getenv("LATITUDE", "0.0"))
LONGITUDE = float(os.getenv("LONGITUDE", "0.0"))
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "")
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", "10"))
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY", "")
TOMMOROWAPI_KEY = os.getenv("TOMMOROWAPI_KEY", "")
METEOSOURCEAPI_KEY = os.getenv("METEOSOURCEAPI_KEY", "")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH", "/app/data/weather_log.csv")
# ===========================================================

def check_open_meteo():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=precipitation"
    try:
        res = requests.get(url, timeout=5)
        data = res.json().get('current', {})
        return data.get('precipitation', 0.0)
    except Exception as e:
        print(f"Błąd Open-Meteo: {e}")
        return 0.0

def check_weather_api():
    if not WEATHERAPI_KEY:
        print("Brak klucza WEATHERAPI_KEY w zmiennych środowiskowych!")
        return "Brak Klucza"
        
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={WEATHERAPI_KEY}"
    try:
        res = requests.get(url, timeout=5)
        weather_list = res.json().get('weather', [{}])
        if weather_list:
            return weather_list[0].get('main', 'N/A')
        return "N/A"
    except Exception as e:
        print(f"Błąd WeatherAPI: {e}")
        return "Błąd"

def check_tommorow_api():
    if not TOMMOROWAPI_KEY:
        print("Brak klucza TOMMOROWAPI_KEY w zmiennych środowiskowych!")
        return 0.0
        
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={LATITUDE},{LONGITUDE}&apikey={TOMMOROWAPI_KEY}"
    try:
        res = requests.get(url, timeout=5)
        values = res.json().get('data', {}).get('values', {})
        return values.get('rainIntensity', 0.0)
    except Exception as e:
        print(f"Błąd TommorowAPI: {e}")
        return 0.0

def check_meteosource_api():
    if not METEOSOURCEAPI_KEY:
        print("Brak klucza METEOSOURCEAPI_KEY w zmiennych środowiskowych!")
        return 0.0
        
    url = f"https://www.meteosource.com/api/v1/free/point?lat={LATITUDE}&lon={LONGITUDE}&sections=current&language=en&units=metric&key={METEOSOURCEAPI_KEY}"
    try:
        res = requests.get(url, timeout=5)
        return res.json().get('current', {}).get('precipitation', {}).get('total', 0.0)
    except Exception as e:
        print(f"Błąd MeteosourceAPI: {e}")
        return 0.0


def save_to_csv(timestamp, om_precip, ow_cond, tom_precip, ms_precip):
    # Tworzenie folderu nadrzędnego, jeśli nie istnieje (przydatne przy testach lokalnych)
    os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)
    
    file_exists = os.path.exists(CSV_FILE_PATH)
    
    with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Zapisz nagłówki, jeśli plik dopiero został utworzony
        if not file_exists:
            writer.writerow([
                "Data_i_Godzina", 
                "OpenMeteo_mm",
                "OpenWeather_cond",
                "Tomorrow_mm",
                "Meteosource_mm"
            ])
            
        # Zapisz zebrane dane
        writer.writerow([
            timestamp, 
            om_precip, 
            ow_cond, 
            tom_precip, 
            ms_precip
        ])
        
def main_loop():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    om_precip = check_open_meteo()
    ow_cond = check_weather_api()
    tom_precip = check_tommorow_api()
    ms_precip = check_meteosource_api()
    save_to_csv(now_str, om_precip, ow_cond, tom_precip, ms_precip)
    print(f"[{now_str}] Zakończono sprawdzanie API. Zapisano dane do pliku CSV.")

if __name__ == "__main__":
    while True:
        print(f"Rozpoczynam sprawdzanie API o {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        main_loop()
        print(f"Odczekaj {INTERVAL_MINUTES} minut przed kolejnym sprawdzeniem.")
        time.sleep(INTERVAL_MINUTES * 60)