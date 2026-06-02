import os
import requests
import pandas as pd
import ta

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

# Delta ETHUSD candles
url = "https://api.delta.exchange/v2/history/candles"

params = {
    "symbol": "ETHUSD",
    "resolution": "15m",
    "limit": 200
}

r = requests.get(url, params=params)
data = r.json()

candles = data["result"]

df = pd.DataFrame(candles)

df["close"] = pd.to_numeric(df["close"])

df["ema21"] = ta.trend.EMAIndicator(
    df["close"],
    window=21
).ema_indicator()

df["ema50"] = ta.trend.EMAIndicator(
    df["close"],
    window=50
).ema_indicator()

df["rsi"] = ta.momentum.RSIIndicator(
    df["close"],
    window=14
).rsi()

price = df["close"].iloc[-1]
ema21 = df["ema21"].iloc[-1]
ema50 = df["ema50"].iloc[-1]
rsi = df["rsi"].iloc[-1]

print("Price:", price)
print("EMA21:", ema21)
print("EMA50:", ema50)
print("RSI:", rsi)

# BUY Setup
if ema21 > ema50 and rsi > 55:
    send_telegram(
        f"""
🟢 ETH BUY SETUP

Price: {price:.2f}

EMA21 > EMA50
RSI: {rsi:.2f}

Paper Trade Signal
"""
    )

# SELL Setup
elif ema21 < ema50 and rsi < 45:
    send_telegram(
        f"""
🔴 ETH SELL SETUP

Price: {price:.2f}

EMA21 < EMA50
RSI: {rsi:.2f}

Paper Trade Signal
"""
    )

else:
    print("No signal")
