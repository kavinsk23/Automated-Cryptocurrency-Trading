import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Load the dataset
df = pd.read_csv('venv/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv')

# Convert the 'Timestamp' column to datetime format and set as index
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
df.set_index('Timestamp', inplace=True)

# Resample the data to 1-hour frequency and select OHLC and volume columns
hourly_df = df.resample('1h').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume_(BTC)': 'sum',
    'Volume_(Currency)': 'sum'
})

# Filter the data to only include the last year
max_date = hourly_df.index.max()
start_date = max_date - pd.DateOffset(years=1)
hourly_df_last_year = hourly_df[(hourly_df.index >= start_date) & (hourly_df.index <= max_date)].copy()

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Apply RSI function to the 'Close' column for the last year
hourly_df_last_year['RSI'] = calculate_rsi(hourly_df_last_year['Close'])

# Calculate Moving Averages
hourly_df_last_year['50MA'] = hourly_df_last_year['Close'].rolling(window=50).mean()
hourly_df_last_year['100MA'] = hourly_df_last_year['Close'].rolling(window=100).mean()
hourly_df_last_year['200MA'] = hourly_df_last_year['Close'].rolling(window=200).mean()

# Calculate Bollinger Bands
hourly_df_last_year['middle_band'] = hourly_df_last_year['Close'].rolling(window=20).mean()
hourly_df_last_year['std_dev'] = hourly_df_last_year['Close'].rolling(window=20).std()
hourly_df_last_year['upper_band'] = hourly_df_last_year['middle_band'] + (hourly_df_last_year['std_dev'] * 2)
hourly_df_last_year['lower_band'] = hourly_df_last_year['middle_band'] - (hourly_df_last_year['std_dev'] * 2)

# Create subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, subplot_titles=('Bitcoin Prices Last Year', 'RSI'))

# Add the candlestick chart for the last year
fig.add_trace(go.Candlestick(x=hourly_df_last_year.index,
                             open=hourly_df_last_year['Open'],
                             high=hourly_df_last_year['High'],
                             low=hourly_df_last_year['Low'],
                             close=hourly_df_last_year['Close'],
                             name="Candlestick"), row=1, col=1)

# Plot Moving Averages
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['50MA'], line=dict(color='gold', width=1), name='50MA'), row=1, col=1)
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['100MA'], line=dict(color='green', width=1), name='100MA'), row=1, col=1)
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['200MA'], line=dict(color='red', width=1), name='200MA'), row=1, col=1)

# Add Bollinger Bands traces
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['upper_band'], line=dict(color='rgba(0,0,255,0.2)'), name='Upper Band'), row=1, col=1)
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['middle_band'], line=dict(color='rgba(0,0,255,0.5)'), name='Middle Band'), row=1, col=1)
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['lower_band'], line=dict(color='rgba(0,0,255,0.2)'), fill='tonexty', name='Lower Band'), row=1, col=1)

# Add RSI trace for the last year
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['RSI'], line=dict(color='blue'), name='RSI'), row=2, col=1)

# Update layout
fig.update_layout(title='Bitcoin Prices, RSI, and Moving Averages for the Last Year', xaxis_title='Time', yaxis_title='Price (USD)')
fig.update_yaxes(title_text="RSI", row=2, col=1)

# Generate HTML string using plotly.io.to_html
plot_div = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

# Save the HTML string to an HTML file
with open('index.html', 'w') as f:
    f.write(plot_div)
