import requests

BASE_URL = "https://api.carbonintensity.org.uk/intensity/date"


def fetch_day(date_str):
    url = f"{BASE_URL}/{date_str}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    return response.json()

def main():
    payload = fetch_day("2026-09-29")
    for reading in payload["data"]:
        forecast = reading["intensity"]["forecast"]
        actual = reading["intensity"]["actual"]
        index = reading["intensity"]["index"]
        print(f"{reading['from']} -> forecast {forecast}, actual {actual}, index {index}")
if __name__ == "__main__":
    main()