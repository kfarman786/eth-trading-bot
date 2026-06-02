import os
import requests
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

message = f"""
✅ ETH Bot Connected

Time:
{datetime.utcnow()}

GitHub Actions is working.
"""

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Telegram test sent.")
