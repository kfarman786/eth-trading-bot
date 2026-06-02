import time
import requests

end_time = int(time.time())
start_time = end_time - (86400 * 7)

url = "https://api.india.delta.exchange/v2/history/candles"

params = {
    "symbol": "ETHUSD",
    "resolution": "1h",
    "start": start_time,
    "end": end_time
}

r = requests.get(url, params=params)

print("STATUS:", r.status_code)
print(r.url)
print(r.json())
