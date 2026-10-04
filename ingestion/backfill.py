import requests
import json
from pathlib import Path
BASE_URL = "https://api.carbonintensity.org.uk/intensity/date"
BRONZE_DIR = Path("data/bronze/intensity_daily")


def fetch_day(date_str):
    url = f"{BASE_URL}/{date_str}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    return response.json()
def save_day(payload,date_str):
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = BRONZE_DIR / (date_str + ".json")
    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)
    return file_path
def main():
    date_str = "2026-09-29"
    payload = fetch_day("2026-09-29")
    path = save_day(payload,date_str)
    print(f"Saved raw data to {path}")
    for reading in payload["data"]:
        forecast = reading["intensity"]["forecast"]
        actual = reading["intensity"]["actual"]
        index = reading["intensity"]["index"]
        print(f"{reading['from']} -> forecast {forecast}, actual {actual}, index {index}")
if __name__ == "__main__":
    main()



