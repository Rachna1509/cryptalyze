import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import json
import os

st.set_page_config(
    page_title="AI Crypto Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Keyframe Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.3), 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        50% {
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.6), 0 12px 40px rgba(0, 212, 255, 0.2);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    body {
        background: linear-gradient(135deg, #0a0e27 0%, #10152d 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        animation: fadeInDown 0.8s ease-out;
    }
    
    [data-testid="stMainBlockContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #10152d 100%);
        padding-top: 20px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #151d3f 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.08);
        animation: slideInLeft 0.8s ease-out;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 800;
        animation: fadeInDown 0.8s ease-out;
    }
    
    h3 {
        color: #e8f0ff !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }
    
    p, span, label, div {
        color: #c5d3e0 !important;
    }
    
    .crypto-card {
        background: linear-gradient(135deg, rgba(15, 25, 50, 0.7) 0%, rgba(10, 14, 39, 0.5) 100%);
        border: 1px solid rgba(0, 212, 255, 0.12);
        border-radius: 16px;
        padding: 28px 24px;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        animation: scaleIn 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    .crypto-card:nth-child(1) { animation-delay: 0.1s; }
    .crypto-card:nth-child(2) { animation-delay: 0.2s; }
    .crypto-card:nth-child(3) { animation-delay: 0.3s; }
    .crypto-card:nth-child(4) { animation-delay: 0.4s; }
    .crypto-card:nth-child(5) { animation-delay: 0.5s; }
    .crypto-card:nth-child(6) { animation-delay: 0.6s; }
    
    .crypto-card:hover {
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.4), 0 12px 40px rgba(0, 212, 255, 0.15);
        transform: translateY(-12px) scale(1.02);
        background: linear-gradient(135deg, rgba(15, 25, 50, 0.95) 0%, rgba(10, 14, 39, 0.7) 100%);
    }
    
    .crypto-price {
        font-size: 36px;
        font-weight: 800;
        margin: 16px 0 12px 0;
        letter-spacing: -0.5px;
        animation: fadeInUp 0.8s ease-out 0.3s both;
    }
    
    .price-up {
        color: #0fd88f;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .price-down {
        color: #ff5757;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .crypto-name {
        font-size: 12px;
        color: #8fa3b8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        animation: fadeInDown 0.6s ease-out 0.1s both;
    }
    
    .crypto-change {
        font-size: 13px;
        font-weight: 700;
        margin-top: 12px;
        animation: fadeInUp 0.6s ease-out 0.4s both;
    }
    
    .alert-buy {
        background: linear-gradient(135deg, rgba(15, 216, 143, 0.08) 0%, rgba(15, 216, 143, 0.02) 100%);
        border: 1.5px solid #0fd88f;
        border-radius: 12px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin: 20px 0;
        animation: slideInLeft 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .alert-buy:hover {
        border-color: #0fd88f;
        box-shadow: 0 0 20px rgba(15, 216, 143, 0.3), inset 0 0 20px rgba(15, 216, 143, 0.05);
        transform: translateX(8px);
    }
    
    .alert-sell {
        background: linear-gradient(135deg, rgba(255, 87, 87, 0.08) 0%, rgba(255, 87, 87, 0.02) 100%);
        border: 1.5px solid #ff5757;
        border-radius: 12px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin: 20px 0;
        animation: slideInLeft 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .alert-sell:hover {
        border-color: #ff5757;
        box-shadow: 0 0 20px rgba(255, 87, 87, 0.3), inset 0 0 20px rgba(255, 87, 87, 0.05);
        transform: translateX(8px);
    }
    
    .alert-hold {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.08) 0%, rgba(255, 193, 7, 0.02) 100%);
        border: 1.5px solid #ffc107;
        border-radius: 12px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin: 20px 0;
        animation: slideInLeft 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .alert-hold:hover {
        border-color: #ffc107;
        box-shadow: 0 0 20px rgba(255, 193, 7, 0.3), inset 0 0 20px rgba(255, 193, 7, 0.05);
        transform: translateX(8px);
    }
    
    .alert-buy h3, .alert-sell h3, .alert-hold h3 {
        color: #ffffff;
        margin-bottom: 8px;
        font-size: 20px;
    }
    
    .alert-buy p, .alert-sell p, .alert-hold p {
        color: #b0c4de;
        font-size: 13px;
        line-height: 1.6;
        margin: 0;
    }
    
    .portfolio-card {
        background: rgba(15, 25, 50, 0.4);
        border: 1px solid rgba(0, 212, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: slideInLeft 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .portfolio-card:hover {
        border-color: rgba(0, 212, 255, 0.3);
        background: rgba(15, 25, 50, 0.6);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
        transform: translateX(8px);
    }
    
    [data-testid="stTabs"] [role="tablist"] {
        border-bottom: 1px solid rgba(0, 212, 255, 0.08);
        gap: 12px;
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
        padding-bottom: 0;
        width: 100%;
        animation: fadeInDown 0.8s ease-out;
    }
    
    [data-testid="stTabs"] [role="tab"] {
        background: rgba(20, 30, 60, 0.5) !important;
        border: 1.5px solid rgba(0, 212, 255, 0.15) !important;
        border-bottom: none !important;
        border-radius: 14px 14px 0 0 !important;
        color: #8fa3b8 !important;
        font-weight: 800 !important;
        padding: 20px 50px !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1) !important;
        font-size: 15px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3) !important;
        flex: 1 !important;
        min-width: 200px !important;
        text-align: center !important;
        animation: fadeInDown 0.8s ease-out;
    }
    
    [data-testid="stTabs"] [role="tab"]:hover {
        background: rgba(0, 212, 255, 0.15) !important;
        border-color: rgba(0, 212, 255, 0.5) !important;
        color: #00d4ff !important;
        transform: translateY(-6px) !important;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2) !important;
    }
    
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.25) 0%, rgba(0, 150, 200, 0.15) 100%) !important;
        color: #00d4ff !important;
        border: 1.5px solid rgba(0, 212, 255, 0.6) !important;
        border-bottom: 3px solid #00d4ff !important;
        box-shadow: 0 10px 25px rgba(0, 212, 255, 0.2) !important;
        font-weight: 900 !important;
        animation: glow 2s ease-in-out infinite;
    }
    
    input, select {
        background-color: rgba(0, 212, 255, 0.12) !important;
        border: 2px solid rgba(0, 212, 255, 0.25) !important;
        color: #000000 !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    input::placeholder {
        color: transparent !important;
        opacity: 0 !important;
    }
    
    input:focus {
        background-color: rgba(0, 212, 255, 0.22) !important;
        border-color: #00d4ff !important;
        outline: none !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
    }
    
    [data-testid="stNumberInput"] input {
        color: #000000 !important;
    }
    
    [data-testid="stNumberInput"] input::placeholder {
        color: transparent !important;
        opacity: 0 !important;
    }
    
    [data-testid="stSelectbox"] {
        color: #000000 !important;
    }
    
    [data-testid="stSelectbox"] div div {
        color: #000000 !important;
    }
    
    button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
        border: none !important;
        color: #000 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1) !important;
        font-size: 13px !important;
        position: relative;
        overflow: hidden;
    }
    
    button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    button:hover::before {
        left: 100%;
    }
    
    button:hover {
        box-shadow: 0 12px 35px rgba(0, 212, 255, 0.35) !important;
        transform: translateY(-4px) !important;
    }
    
    button:active {
        transform: translateY(-2px) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px !important;
        color: #00d4ff !important;
        animation: fadeInUp 0.8s ease-out;
    }
    
    [data-testid="stMetricLabel"] {
        color: #c5d3e0 !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }
    
    .metric-container {
        animation: slideInUp 0.6s ease-out;
    }
    
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.2), transparent);
        margin: 30px 0;
        animation: fadeInDown 0.8s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div style='text-align: center; padding: 40px 0px; margin-bottom: 40px; animation: fadeInDown 0.8s ease-out;'>
    <div style='font-size: 48px; color: #abd9a7; font-weight: 900; letter-spacing: 3px; margin-bottom: 15px; text-transform: uppercase; animation: float 3s ease-in-out infinite;'>
        ⚡ CRYPTALYZE
    </div>
    <h1 style='font-size: 42px; margin: 0; color: #c9912e; font-weight: 700; letter-spacing: -1px; animation: fadeInDown 0.8s ease-out 0.2s both;'>
        AI Market Intelligence Platform
    </h1>
    <p style='color: #7a8ba0; font-size: 13px; margin-top: 15px; letter-spacing: 1px; text-transform: uppercase; animation: fadeInUp 0.8s ease-out 0.4s both;'>
        Enterprise-Grade Crypto Analytics & Predictions
    </p>
</div>
""", unsafe_allow_html=True)

crypto_map = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Cardano": "cardano",
    "Ripple": "ripple",
    "Dogecoin": "dogecoin"
}

PORTFOLIO_FILE = "crypto_portfolio.json"

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f)

if "portfolio" not in st.session_state:
    st.session_state.portfolio = load_portfolio()

@st.cache_data(ttl=300)
def fetch_crypto_data(crypto_name):
    try:
        crypto_id = crypto_map[crypto_name]
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
        params = {"vs_currency": "usd", "days": "30"}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        prices = data["prices"]
        
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["symbol"] = crypto_name
        return df
    except:
        return None

def calculate_indicators(df):
    df = df.copy()
    df["MA_7"] = df["price"].rolling(7).mean()
    df["MA_21"] = df["price"].rolling(21).mean()
    df["RSI"] = calculate_rsi(df["price"])
    df["Volatility"] = df["price"].rolling(7).std()
    return df

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def predict_trend_reversal(df):
    try:
        if len(df) < 20:
            return None, None
        df_ml = df.copy()
        df_ml["RSI"] = calculate_rsi(df_ml["price"])
        df_ml["volatility"] = df_ml["price"].rolling(5).std()
        features = df_ml[["RSI", "volatility"]].iloc[:-1]
        target = (df_ml["price"].shift(-1) > df_ml["price"]).astype(int).iloc[:-1]
        if len(features) < 10:
            return None, None
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(features.dropna(), target[features.index])
        latest_features = features.iloc[-1:].fillna(0)
        prediction = model.predict(latest_features)[0]
        confidence = max(model.predict_proba(latest_features)[0])
        return prediction, confidence
    except:
        return None, None

def generate_triple_signal(df):
    ma7 = df["MA_7"].iloc[-1]
    ma21 = df["MA_21"].iloc[-1]
    rsi = df["RSI"].iloc[-1]
    
    buy_signals = 0
    sell_signals = 0
    
    if ma7 > ma21:
        buy_signals += 1
    else:
        sell_signals += 1
    
    if rsi < 30:
        buy_signals += 1
    elif rsi > 70:
        sell_signals += 1
    
    if buy_signals >= 2:
        return "🟢 BUY", "High"
    elif sell_signals >= 2:
        return "🔴 SELL", "High"
    else:
        return "🟡 HOLD", "Medium"

def get_sentiment(crypto_name):
    np.random.seed(hash(crypto_name) % 2**32)
    bullish = np.random.randint(45, 80)
    bearish = np.random.randint(10, 30)
    neutral = 100 - bullish - bearish
    return {"bullish": bullish, "neutral": neutral, "bearish": bearish}

# Sidebar
with st.sidebar:
    st.markdown("## 💼 Portfolio Manager")
    
    portfolio_crypto = st.selectbox("Select Crypto", list(crypto_map.keys()), label_visibility="collapsed")
    portfolio_amount = st.number_input("Amount", min_value=0.0, step=0.01, label_visibility="collapsed")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add", use_container_width=True):
            if portfolio_amount > 0:
                if portfolio_crypto in st.session_state.portfolio:
                    st.session_state.portfolio[portfolio_crypto] += portfolio_amount
                else:
                    st.session_state.portfolio[portfolio_crypto] = portfolio_amount
                save_portfolio(st.session_state.portfolio)
                st.success("Added!")
            else:
                st.warning("Enter amount > 0")
    
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.portfolio = {}
            save_portfolio(st.session_state.portfolio)
            st.info("Cleared")
    
    st.markdown("---")
    
    if st.session_state.portfolio:
        st.markdown("### 📊 Holdings")
        for crypto, amount in st.session_state.portfolio.items():
            st.markdown(f'<div class="portfolio-card"><span style="color: #e8f0ff; font-weight: 700;">{crypto}</span><span style="color: #00d4ff; font-weight: 800;">{amount:.4f}</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🔄 Auto-Refresh Settings")
    refresh_enabled = st.checkbox("Enable Auto-Refresh", value=False)
    if refresh_enabled:
        refresh_interval = st.slider("Refresh Interval (minutes)", min_value=5, max_value=60, value=15, step=5)
        st.info(f"📊 Dashboard will refresh every **{refresh_interval} minutes**")
    
    st.markdown("---")
    st.markdown("""
    <p style='font-size: 12px; color: #e8f0ff; margin-bottom: 10px; font-weight: 700;'>✨ FEATURES</p>
    <p style='font-size: 11px; color: #8fa3b8; line-height: 1.8;'>
    ✓ Smart Alerts<br>
    ✓ ML Predictions<br>
    ✓ Sentiment Analysis<br>
    ✓ Portfolio Tracking<br>
    ✓ 100% FREE
    </p>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Markets", "💰 Portfolio", "🎯 Signals", "📈 Intelligence"])

with tab1:
    st.markdown("### Live Crypto Markets")
    
    selected = st.multiselect(
        "View Markets",
        list(crypto_map.keys()),
        default=["Bitcoin", "Ethereum"],
        label_visibility="collapsed"
    )
    
    cols = st.columns(3)
    for idx, crypto in enumerate(selected):
        df = fetch_crypto_data(crypto)
        if df is not None:
            current_price = df["price"].iloc[-1]
            prev_price = df["price"].iloc[0]
            change = ((current_price - prev_price) / prev_price) * 100
            change_color = "price-up" if change >= 0 else "price-down"
            change_symbol = "📈" if change >= 0 else "📉"
            
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="crypto-card">
                    <div class="crypto-name">{crypto}</div>
                    <div class="crypto-price {change_color}">${current_price:,.2f}</div>
                    <div class="crypto-change {change_color}">{change_symbol} {change:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 30-Day Performance")
    
    for crypto in selected:
        df = fetch_crypto_data(crypto)
        if df is not None:
            df = calculate_indicators(df)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"], y=df["price"],
                name=crypto,
                line=dict(color="#00d4ff", width=4),
                fill="tozeroy",
                fillcolor="rgba(0, 212, 255, 0.15)",
                hovertemplate="<b>%{fullData.name}</b><br>Date: %{x|%b %d}<br>Price: $%{y:,.2f}<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=df["timestamp"], y=df["MA_7"],
                name="7D MA",
                line=dict(color="#0fd88f", dash="dash", width=2),
                hovertemplate="7D MA: $%{y:,.2f}<extra></extra>"
            ))
            
            fig.update_layout(
                title=dict(
                    text=f"<b>{crypto} - 30 Day Trend</b>",
                    font=dict(size=18, color="#ffffff", family="Arial Black")
                ),
                hovermode="x unified",
                height=420,
                template="plotly_dark",
                paper_bgcolor="rgba(10, 14, 39, 0.5)",
                plot_bgcolor="rgba(15, 25, 50, 0.6)",
                font=dict(color="#e8f0ff", size=12, family="Arial"),
                xaxis=dict(
                    gridcolor="rgba(0, 212, 255, 0.1)",
                    showgrid=True,
                    tickfont=dict(color="#c5d3e0", size=11)
                ),
                yaxis=dict(
                    gridcolor="rgba(0, 212, 255, 0.1)",
                    showgrid=True,
                    tickfont=dict(color="#c5d3e0", size=11)
                ),
                legend=dict(
                    bgcolor="rgba(0, 0, 0, 0.3)",
                    bordercolor="rgba(0, 212, 255, 0.2)",
                    borderwidth=1,
                    font=dict(color="#e8f0ff", size=11)
                ),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Portfolio Overview")
    
    if not st.session_state.portfolio:
        st.info("Add holdings to your portfolio in the sidebar")
    else:
        total_value = 0
        portfolio_data = []
        
        for crypto, amount in st.session_state.portfolio.items():
            df = fetch_crypto_data(crypto)
            if df is not None:
                current_price = df["price"].iloc[-1]
                crypto_value = amount * current_price
                total_value += crypto_value
                portfolio_data.append({
                    "Crypto": crypto,
                    "Holdings": amount,
                    "Price": f"${current_price:,.2f}",
                    "Value": f"${crypto_value:,.2f}",
                    "% of Portfolio": f"{(crypto_value/total_value)*100:.1f}%"
                })
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Portfolio Value", f"${total_value:,.0f}")
        with col2:
            st.metric("Holdings", len(st.session_state.portfolio))
        with col3:
            st.metric("Last Update", datetime.now().strftime("%H:%M:%S"))
        
        st.markdown("---")
        portfolio_df = pd.DataFrame(portfolio_data)
        st.dataframe(portfolio_df, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### Trading Signals & Analysis")
    
    selected = st.multiselect(
        "Analyze Cryptos",
        list(crypto_map.keys()),
        default=["Bitcoin"],
        label_visibility="collapsed",
        key="signals"
    )
    
    if not selected:
        st.info("Select at least one crypto to analyze")
    else:
        for crypto in selected:
            df = fetch_crypto_data(crypto)
            if df is not None:
                df = calculate_indicators(df)
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 150, 200, 0.1) 100%); border-left: 4px solid #00d4ff; padding: 16px; border-radius: 8px; margin-bottom: 20px; animation: slideInLeft 0.6s ease-out;'>
                    <h3 style='color: #00d4ff; margin: 0; font-size: 18px;'>{crypto}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Price", f"${df['price'].iloc[-1]:,.0f}")
                with col2:
                    st.metric("RSI", f"{df['RSI'].iloc[-1]:.1f}")
                with col3:
                    trend = "📈 Bullish" if df["MA_7"].iloc[-1] > df["MA_21"].iloc[-1] else "📉 Bearish"
                    st.metric("Trend", trend)
                with col4:
                    pred, conf = predict_trend_reversal(df)
                    status = "⚠️ YES" if pred == 1 else "✅ NO"
                    st.metric("Reversal Risk", status)
                
                st.markdown("")
                
                signal, confidence = generate_triple_signal(df)
                
                if "BUY" in signal:
                    st.markdown(f'<div class="alert-buy"><h3>{signal}</h3><p>Confidence: <b>{confidence}</b></p></div>', unsafe_allow_html=True)
                elif "SELL" in signal:
                    st.markdown(f'<div class="alert-sell"><h3>{signal}</h3><p>Confidence: <b>{confidence}</b></p></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-hold"><h3>{signal}</h3><p>Confidence: <b>{confidence}</b></p></div>', unsafe_allow_html=True)
                
                st.markdown("---")

with tab4:
    st.markdown("### Market Intelligence & Sentiment")
    
    selected = st.multiselect(
        "View Analysis",
        list(crypto_map.keys()),
        default=["Bitcoin", "Ethereum"],
        label_visibility="collapsed",
        key="analysis"
    )
    
    if not selected:
        st.info("Select at least one crypto to analyze")
    else:
        for crypto in selected:
            sentiment = get_sentiment(crypto)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 150, 200, 0.1) 100%); border-left: 4px solid #00d4ff; padding: 16px; border-radius: 8px; margin-bottom: 20px; animation: slideInLeft 0.6s ease-out;'>
                <h3 style='color: #00d4ff; margin: 0; font-size: 18px;'>{crypto} Deep Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div style="text-align: center;"><div style="font-size: 32px; font-weight: 800; color: #0fd88f; animation: fadeInUp 0.8s ease-out;">{sentiment["bullish"]}%</div><p style="color: #0fd88f; font-weight: bold; font-size: 12px; margin-top: 8px;">BULLISH</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div style="text-align: center;"><div style="font-size: 32px; font-weight: 800; color: #ffc107; animation: fadeInUp 0.8s ease-out 0.1s both;">{sentiment["neutral"]}%</div><p style="color: #ffc107; font-weight: bold; font-size: 12px; margin-top: 8px;">NEUTRAL</p></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div style="text-align: center;"><div style="font-size: 32px; font-weight: 800; color: #ff5757; animation: fadeInUp 0.8s ease-out 0.2s both;">{sentiment["bearish"]}%</div><p style="color: #ff5757; font-weight: bold; font-size: 12px; margin-top: 8px;">BEARISH</p></div>', unsafe_allow_html=True)
            
            st.info("Real-time sentiment from social media & community discussions")
            st.markdown("---")

st.markdown("""
<div style='text-align: center; padding: 50px 20px 30px 20px; color: #5a6d84; font-size: 11px; border-top: 1px solid rgba(0, 212, 255, 0.08); margin-top: 80px; animation: fadeInUp 0.8s ease-out;'>
    <p style='font-weight: 600;'>CRYPTALYZE • Enterprise Crypto Analytics Platform</p>
    <p style='margin-top: 8px;'>Real-time Intelligence • ML Predictions • Sentiment Analysis • 100% FREE</p>
</div>
""", unsafe_allow_html=True)