import json

with open("paper_trades.json", "r") as f:
    data = json.load(f)

print("Balance:", data["balance"])
print("Wins:", data["wins"])
print("Losses:", data["losses"])
print("Open Trade:", data["open_trade"])
