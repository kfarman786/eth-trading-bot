import os
import requests

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
            "days": "2",
            "interval": "hourly"
        },
        timeout=20
    )

    data = r.json()

    prices = [p[1] for p in data["prices"]]

    current_price = prices[-1]

    sma20 = sum(prices[-20:]) / 20

    print("Price:", current_price)
    print("SMA20:", sma20)

    if current_price > sma20:

        send(
            f"🚀 ETH BUY WATCH\n\n"
            f"Price: ${current_price:.2f}\n"
            f"SMA20: ${sma20:.2f}\n\n"
            f"Trend appears bullish."
        )

        print("BUY signal sent")

    else:
        print("No signal")

except Exception as e:
    print("ERROR:", str(e))
