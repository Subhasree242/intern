import requests

API_KEY = "E6VTTLWAQQWI6A00"

url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AAPL",
    "apikey": API_KEY
}

data = requests.get(url, params=params).json()
print(data)
