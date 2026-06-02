import os
import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

try:
    url = "https://api.binance.com/api/v3/klines"
    
    params = {
        "symbol": "ETHUSDT",
        "interval": "15m",
        "limit": 100
    }

    r = requests.get(url, params=params, timeout=20)
    data = r.json()

    closes = [float(x[4]) for x in data]

    df = pd.DataFrame()
    df["close"] = closes

    ema21 = EMAIndicator(df["close"], window=21).ema_indicator()
    ema50 = EMAIndicator(df["close"], window=50).ema_indicator()

    rsi = RSIIndicator(df["close"], window=14).rsi()

    current_price = closes[-1]

    current_ema21 = round(ema21.iloc[-1], 2)
    current_ema50 = round(ema50.iloc[-1], 2)
    current_rsi = round(rsi.iloc[-1], 2)

    if current_ema21 > current_ema50 and 45 <= current_rsi <= 65:

        msg = f"""
🚀 ETH SIGNAL

Price: {current_price}

EMA21: {current_ema21}
EMA50: {current_ema50}

RSI: {current_rsi}

Bullish setup detected.
"""

        send_telegram(msg)

    print("Bot completed.")

except Exception as e:
    print("ERROR:", e)
