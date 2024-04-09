import requests

API_KEY = 'S9BCX4BJJOONO1TV'  # Your Alpha Vantage API Key
SYMBOL = 'AAPL'  # Stock symbol, e.g., AAPL for Apple Inc.
INTERVAL = 'daily'  # Interval could be 1min, 5min, 15min, 30min, 60min, daily, weekly, or monthly
TIME_PERIOD = 14  # Commonly used tinme period for RSI calculation
SERIES_TYPE = 'close'  # The type of price data to use (close, open, high, low)

# Update the URL to use the RSI function
url = f"https://www.alphavantage.co/query?function=RSI&symbol={SYMBOL}&interval={INTERVAL}&time_period={TIME_PERIOD}&series_type={SERIES_TYPE}&apikey={API_KEY}"

response = requests.get(url)
data = response.json()

print(data)
