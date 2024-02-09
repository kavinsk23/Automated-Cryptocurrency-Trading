import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Load the dataset
df = pd.read_csv('venv/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv')

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Set the 'Timestamp' as the index
df.set_index('Timestamp', inplace=True)

# Resample the data to 1-hour frequency and select OHLC and volume columns
hourly_df = df.resample('1h').agg({'Open': 'first',
                                   'High': 'max',
                                   'Low': 'min',
                                   'Close': 'last',
                                   'Volume_(BTC)': 'sum',
                                   'Volume_(Currency)': 'sum'})

# Filter the data to only include the last year and explicitly create a new DataFrame
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

# Simplified heuristic for identifying order blocks
def find_order_blocks(df, window=14):
    df['range'] = df['High'] - df['Low']
    df['is_order_block'] = (df['range'].shift(1) > df['range'].rolling(window=window).mean()) & (df['range'] < df['range'].rolling(window=window).mean())
    return df[df['is_order_block']]

# Find potential order blocks
order_blocks = find_order_blocks(hourly_df_last_year)

# Create subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, subplot_titles=('Bitcoin Prices Last Year', 'RSI'))

# Add the candlestick chart for the last year
fig.add_trace(go.Candlestick(x=hourly_df_last_year.index,
                             open=hourly_df_last_year['Open'],
                             high=hourly_df_last_year['High'],
                             low=hourly_df_last_year['Low'],
                             close=hourly_df_last_year['Close'],
                             name="Candlestick"), row=1, col=1)

# Add RSI trace for the last year
fig.add_trace(go.Scatter(x=hourly_df_last_year.index, y=hourly_df_last_year['RSI'], line=dict(color='blue'), name='RSI'), row=2, col=1)

# # Plot order blocks with light blue color
# for index, row in order_blocks.iterrows():
#     fig.add_trace(go.Scatter(x=[index, index], y=[row['Low'], row['High']], mode='lines', line=dict(color='lightblue', width=2), name='Order Block'), row=1, col=1)

# Update layout
fig.update_layout(title='Bitcoin Prices and RSI for the Last Year', xaxis_title='Time', yaxis_title='Price (USD)')
fig.update_yaxes(title_text="RSI", row=2, col=1)

# Generate HTML string using plotly.io.to_html
plot_div = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

# Save the HTML string to an HTML file
with open('index.html', 'w') as f:
    f.write(plot_div)
