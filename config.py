import json
from forex_python.converter import CurrencyRates
import time
import requests

CONFIG_FILE = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def get_exchange_rate(currency, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
            response.raise_for_status()
            data = response.json()
            rate = data['rates']['TRY']
            return rate
        except Exception as e:
            print(f"Attempt {attempt + 1} - Error fetching exchange rate for {currency}: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
    
    print(f"Failed to fetch exchange rate for {currency} after {retries} attempts. Using fallback rate.")
    return 1.0  # Fallback exchange rate
