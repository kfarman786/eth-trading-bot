import requests

r = requests.get("https://api.india.delta.exchange/v2/products")

data = r.json()

for p in data["result"]:
    if "ETHUSD" in p.get("symbol", ""):
        print("PRODUCT FOUND")
        print(p)
