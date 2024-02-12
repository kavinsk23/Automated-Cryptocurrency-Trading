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

# Calculate MACD and Signal Line
exp1 = hourly_df_last_year['Close'].ewm(span=12, adjust=False).mean()
exp2 = hourly_df_last_year['Close'].ewm(span=26, adjust=False).mean()
hourly_df_last_year['MACD'] = exp1 - exp2
hourly_df_last_year['Signal_Line'] = hourly_df_last_year['MACD'].ewm(span=9, adjust=False).mean()

# Calculate the Middle Bollinger Band (20-day SMA)
hourly_df_last_year['middle_band'] = hourly_df_last_year['Close'].rolling(window=20).mean()

# Calculate the Standard Deviation
hourly_df_last_year['std_dev'] = hourly_df_last_year['Close'].rolling(window=20).std()

# Calculate the Upper and Lower Bollinger Bands
hourly_df_last_year['upper_band'] = hourly_df_last_year['middle_band'] + (hourly_df_last_year['std_dev'] * 2)
hourly_df_last_year['lower_band'] = hourly_df_last_year['middle_band'] - (hourly_df_last_year['std_dev'] * 2)


# Create subplots
fig = make_subplots(
    rows=3,  # For Candlestick, RSI, and MACD
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.2,  # Adjust spacing to preference
    subplot_titles=('' 'RSI', 'MACD')
)

# Add the candlestick chart
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

# Add RSI trace
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['RSI'], line=dict(color='blue'), name='RSI'), row=2, col=1)

# Add MACD and Signal line traces
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['MACD'], line=dict(color='green'), name='MACD Line'), row=3, col=1)
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['Signal_Line'], line=dict(color='red'), name='Signal Line'), row=3, col=1)

# Add Bollinger Bands traces
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['upper_band'], line=dict(color='rgba(0,0,255,0.2)'), name='Upper Band'), row=1, col=1)
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['middle_band'], line=dict(color='rgba(0,0,255,0.5)'), name='Middle Band'), row=1, col=1)
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['lower_band'], line=dict(color='rgba(0,0,255,0.2)'), fill='tonexty', name='Lower Band'), row=1, col=1)


# Adjust layout for rangeselector
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1H", step="hour", stepmode="backward"),
                dict(count=1, label="1D", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(step="all", label="All data")
            ])
        ),
        type="date"
    ),
    xaxis2=dict(type="date"),
    xaxis3=dict(type="date")
)

# Save the plot as HTML file
plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
with open('plot.html', 'w') as f:
    f.write(plot_html)
