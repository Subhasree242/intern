import requests

API_KEY = "E6VTTLWAQQWI6A00"

keyword = "RELIANCE"   # try TCS, INFY, HDFC etc.
url = "https://www.alphavantage.co/query"

params = {
    "function": "SYMBOL_SEARCH",
    "keywords": keyword,
    "apikey": API_KEY
}

data = requests.get(url, params=params).json()
print(data)
