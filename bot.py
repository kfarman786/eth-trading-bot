import os
import requests

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")

print("API Key Found:", API_KEY is not None)
print("Secret Found:", API_SECRET is not None)

r = requests.get(
    "https://api.india.delta.exchange/v2/products"
)

print("Status:", r.status_code)

data = r.json()

print("Success:", data.get("success"))

if data.get("result"):
    print("Products Found:", len(data["result"]))
    print("First Product:", data["result"][0]["symbol"])
