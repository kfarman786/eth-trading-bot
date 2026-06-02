import os
import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=20
    )

try:
    r = requests.get(
        "https://api.coingecko.com/api/v3/coins/ethereum/market_chart",
        params={
            "vs_currency": "usd",
            "days": "7",
            "interval": "hourly"
        },
        timeout=20
    )

    data = r.json()

    prices = [p[1] for p in data["prices"]]

    df = pd.DataFrame()
    df["close"] = prices

    ema21 = EMAIndicator(df["close"], window=21).ema_indicator()
    ema50 = EMAIndicator(df["close"], window=50).ema_indicator()
    rsi = RSIIndicator(df["close"], window=14).rsi()

    price = float(df["close"].iloc[-1])

    ema21_now = float(ema21.iloc[-1])
    ema50_now = float(ema50.iloc[-1])
    rsi_now = float(rsi.iloc[-1])

    print("Price:", round(price, 2))
    print("EMA21:", round(ema21_now, 2))
    print("EMA50:", round(ema50_now, 2))
    print("RSI:", round(rsi_now, 2))

    bullish = (
        ema21_now > ema50_now and
        45 <= rsi_now <= 65
    )

    if bullish:

        msg = (
            f"🚀 ETH BUY WATCH\n\n"
            f"Price: ${price:.2f}\n"
            f"EMA21: ${ema21_now:.2f}\n"
            f"EMA50: ${ema50_now:.2f}\n"
            f"RSI: {rsi_now:.2f}\n\n"
            f"Trend appears bullish."
        )

        send(msg)

        print("BUY signal sent")

    else:
        print("No signal")

except Exception as e:
    print("ERROR:", str(e))
