import requests

r = requests.get("https://api.india.delta.exchange/v2/products")

data = r.json()

print("TOTAL PRODUCTS:", len(data["result"]))

for p in data["result"]:
    if "ETH" in p.get("symbol", ""):
        print(p)
