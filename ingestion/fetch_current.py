import json
from datetime import datetime, timezone
from pathlib import Path

import requests

URL = "https://api.carbonintensity.org.uk/intensity"
BRONZE_DIR = Path("data/bronze/intensity")


def fetch_current():
    response = requests.get(URL, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    return response.json()


def save_raw(payload):
    now = datetime.now(timezone.utc)
    folder = BRONZE_DIR / now.strftime("%Y-%m-%d")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / (now.strftime("%H%M") + ".json")
    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)
    return file_path


def main():
    payload = fetch_current()
    path = save_raw(payload)
    print(f"Saved raw data to {path}")
    reading = payload["data"][0]
    forecast = reading["intensity"]["forecast"]
    actual = reading["intensity"]["actual"]
    index = reading["intensity"]["index"]
    print(f"{reading['from']} -> forecast {forecast}, actual {actual}, index {index}")


if __name__ == "__main__":
    main()