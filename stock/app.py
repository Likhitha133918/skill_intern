import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. Page Configuration ---
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
st.title(" Stock Analysis & Visualization Dashboard")

# --- 2. Sidebar: Accept User Input ---
st.sidebar.header("User Input Parameters")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()
start_date = st.sidebar.date_input("Start Date", value=datetime.now() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", value=datetime.now())

# Technical Indicator Settings
st.sidebar.subheader("Indicator Settings")
sma_window = st.sidebar.slider("SMA Window", 5, 100, 20)
ema_window = st.sidebar.slider("EMA Window", 5, 100, 20)
rsi_window = st.sidebar.slider("RSI Window", 2, 30, 14)

# --- 3. Fetch Historical Data ---
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)

    # yfinance may return a MultiIndex dataframe (e.g. when a ticker is treated as a list).
    # In that case, select the data for the requested ticker and drop the ticker level.
    if isinstance(data.columns, pd.MultiIndex):
        if ticker in data.columns.get_level_values(1):
            data = data.xs(ticker, axis=1, level=1, drop_level=True)
        else:
            # If ticker is not present, fall back to using first ticker/level
            data.columns = data.columns.get_level_values(0)

    return data

data = load_data(ticker_symbol, start_date, end_date)

if data.empty:
    st.error("No data found. Please check the ticker symbol.")
else:
    # --- 4. Calculate Indicators ---
    # Simple Moving Average (SMA)
    data['SMA'] = data['Close'].rolling(window=sma_window).mean()
    
    # Exponential Moving Average (EMA)
    data['EMA'] = data['Close'].ewm(span=ema_window, adjust=False).mean()
    
    # Relative Strength Index (RSI)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # --- 5. Display Performance Summary ---
    col1, col2, col3, col4 = st.columns(4)
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[-2]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100

    col1.metric("Last Price", f"${last_close:.2f}", f"{change:.2f} ({pct_change:.2f}%)")
    col2.metric("52W High", f"${data['High'].max():.2f}")
    col3.metric("52W Low", f"${data['Low'].min():.2f}")
    col4.metric("Volume", f"{data['Volume'].iloc[-1]:,}")

    # --- 6. Plotting Charts ---
    # Main Price Chart (Candlestick + SMA/EMA)
    fig_price = go.Figure()
    fig_price.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], 
                                     low=data['Low'], close=data['Close'], name="Candlestick"))
    fig_price.add_trace(go.Scatter(x=data.index, y=data['SMA'], line=dict(color='orange', width=2), name=f'SMA {sma_window}'))
    fig_price.add_trace(go.Scatter(x=data.index, y=data['EMA'], line=dict(color='blue', width=2), name=f'EMA {ema_window}'))
    
    fig_price.update_layout(title=f"{ticker_symbol} Price Chart", yaxis_title="Price (USD)", height=600)
    st.plotly_chart(fig_price, use_container_width=True)

    # RSI Chart
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='purple'), name="RSI"))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
    fig_rsi.update_layout(title="RSI (Relative Strength Index)", yaxis_title="Value", height=300)
    st.plotly_chart(fig_rsi, use_container_width=True)

    # --- 7. CSV Export Option ---
    st.subheader("Raw Data & Export")
    st.dataframe(data.tail(10))

    csv = data.to_csv().encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=f'{ticker_symbol}_stock_data.csv',
        mime='text/csv',
    )