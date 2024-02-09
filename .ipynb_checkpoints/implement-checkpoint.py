import pandas as pd
import mplfinance as mpf

# Load the dataset (assuming it's in CSV format)
df = pd.read_csv('venv/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv')

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Resample the data to 1-hour frequency and select OHLC and volume columns
df.set_index('Timestamp', inplace=True)
hourly_df = df.resample('1h').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last',
                                   'Volume_(BTC)': 'sum', 'Volume_(Currency)': 'sum'})

# Combine volume columns into a single 'Volume' column
hourly_df['Volume'] = hourly_df['Volume_(BTC)']

# Plot candlestick chart
mpf.plot(hourly_df, type='line', style='charles', title='Bitcoin Price Chart (1 Day, 1 Hour Intervals)',
         ylabel='Price (USD)', ylabel_lower='Volume (BTC)', volume=True, show_nontrading=True)
