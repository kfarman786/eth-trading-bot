import os
import requests

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")

print("API Key Found:", bool(API_KEY))
print("Secret Found:", bool(API_SECRET))

r = requests.get(
    "https://api.india.delta.exchange/v2/products"
)

print("Status:", r.status_code)

data = r.json()

print("Success:", data["success"])
print("Products Found:", len(data["result"]))
print("First Product:", data["result"][0]["symbol"])
