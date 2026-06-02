import os
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

try:
    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": "ethereum",
            "vs_currencies": "usd"
        },
        timeout=20
    )

    data = r.json()

    price = data["ethereum"]["usd"]

    print("ETH Price:", price)

    msg = f"ETH Price: ${price}"

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=20
    )

    print("Telegram sent")

except Exception as e:
    print("ERROR:", str(e))
