import os
import time
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

try:
    end_time = int(time.time())
    start_time = end_time - (200 * 15 * 60)

    url = "https://api.delta.exchange/v2/history/candles"

    params = {
        "symbol": "ETHUSD",
        "resolution": "15m",
        "start": start_time,
        "end": end_time
    }

    r = requests.get(url, params=params)

    print("STATUS:", r.status_code)

    data = r.json()

    print(data)

    if r.status_code == 200:
        send_telegram("✅ Delta ETHUSD candle connection working")
    else:
        send_telegram(f"❌ Delta API Error: {r.status_code}")

except Exception as e:
    print(e)
    send_telegram(f"❌ Bot Error:\n{e}")
