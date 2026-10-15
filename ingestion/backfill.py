import json
from datetime import date, timedelta
from pathlib import Path

import requests

BASE_URL = "https://api.carbonintensity.org.uk/intensity/date"
REGIONAL_URL = "https://api.carbonintensity.org.uk/regional/intensity"
NATIONAL_DIR = Path("data/bronze/intensity_daily")
REGIONAL_DIR = Path("data/bronze/intensity_regional")


def fetch_day(date_str):
    url = f"{BASE_URL}/{date_str}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    return response.json()


def fetch_regional_day(day):
    next_day = day + timedelta(days=1)
    url = f"{REGIONAL_URL}/{day.isoformat()}T00:00Z/{next_day.isoformat()}T00:00Z"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    return response.json()



def save_day(payload, date_str, folder):
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / (date_str + ".json")
    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)
    return file_path


def main():
    start = date(2026, 9, 1)
    end = date(2026, 9, 30)
    current = start
    while current <= end:
        date_str = current.isoformat()

        payload = fetch_day(date_str)
        path = save_day(payload, date_str, NATIONAL_DIR)
        print(f"Saved raw data to {path}")

        regional_payload = fetch_regional_day(current)
        regional_path = save_day(regional_payload, date_str, REGIONAL_DIR)
        print(f"Saved raw data to {regional_path}")

        current = current + timedelta(days=1)
if __name__ == "__main__":
    main()

