import requests

r = requests.get("https://api.india.delta.exchange/v2/products")

for p in r.json()["result"]:
    symbol = p.get("symbol", "")

    if symbol == "ETHUSD":
        print("FOUND ETHUSD")
        print(p)
