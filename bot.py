import requests

r = requests.get("https://api.india.delta.exchange/v2/products")

for p in r.json()["result"]:
    if p.get("symbol") == "ETHUSD":
        print("PRODUCT ID =", p["id"])
        print("SYMBOL =", p["symbol"])
        break
