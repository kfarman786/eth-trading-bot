import requests

url = "https://api.india.delta.exchange/v2/products/3136"

r = requests.get(url)

print("STATUS:", r.status_code)
print(r.text[:1000])
