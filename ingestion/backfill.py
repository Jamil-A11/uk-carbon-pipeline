import json
from datetime import date, timedelta
from pathlib import Path

import requests

BASE_URL = "https://api.carbonintensity.org.uk/intensity/date"
BRONZE_DIR = Path("data/bronze/intensity_daily")


def fetch_day(date_str):
    url = f"{BASE_URL}/{date_str}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    return response.json()


def save_day(payload, date_str):
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = BRONZE_DIR / (date_str + ".json")
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
        path = save_day(payload, date_str)
        print(f"Saved raw data to {path}")
        current = current + timedelta(days=1)


if __name__ == "__main__":
    main()


