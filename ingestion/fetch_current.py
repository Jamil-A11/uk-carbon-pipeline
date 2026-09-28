import requests

URL = "https://api.carbonintensity.org.uk/intensity"


def fetch_current():
    response = requests.get(URL, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    return response.json()


def main():
    payload = fetch_current()
    reading = payload["data"][0]
    forecast = reading["intensity"]["forecast"]
    actual = reading["intensity"]["actual"]
    index = reading["intensity"]["index"]
    print(f"{reading['from']} -> forecast {forecast}, actual {actual}, index {index}")  


if __name__ == "__main__":
    main()