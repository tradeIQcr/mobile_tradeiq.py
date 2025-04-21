import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objs as go
from datetime import datetime

# Mobile config
st.set_page_config(
    page_title="📱 Crypto TradeIQ",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {padding: 1rem;}
    .stTextInput input {font-size: 16px !important;}
    .plotly-graph-div {width: 100% !important;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# App Header
st.title("📱 Crypto TradeIQ")
st.caption("Your mobile trading assistant")

# Settings
with st.expander("⚙️ Settings"):
    symbol = st.text_input("Symbol (e.g. BTC-USD)", "BTC-USD").upper()
    days = st.slider("Days to show", 30, 365, 90)

# Data Loading
@st.cache_data(ttl=3600)
def load_data(symbol, days):
    end = datetime.today()
    start = end - pd.Timedelta(days=days)
    try:
        return yf.download(symbol, start, end)
    except:
        st.error("Error loading data")
        return None

data = load_data(symbol, days)
if data is None: st.stop()

# Indicators
close = data["Close"].squeeze()
data["RSI"] = ta.momentum.RSIIndicator(close).rsi()
macd = ta.trend.MACD(close)
data["MACD"] = macd.macd()
data["MACD_signal"] = macd.macd_signal()

# Price Chart
st.subheader(f"{symbol} Price")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Price"))
fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10))
st.plotly_chart(fig, use_container_width=True)

# RSI Chart
st.subheader("RSI")
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=data.index, y=data["RSI"], name="RSI"))
fig_rsi.add_hline(y=70, line_dash="dot", line_color="red")
fig_rsi.add_hline(y=30, line_dash="dot", line_color="green")
fig_rsi.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10))
st.plotly_chart(fig_rsi, use_container_width=True)

# Current Price
latest = data["Close"].iloc[-1]
change = latest - data["Close"].iloc[-2]
st.metric(label="Current Price", value=f"${latest:.2f}", 
          delta=f"{change:.2f} ({change/latest:.2%})")
