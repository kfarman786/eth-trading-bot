import json

with open("paper_trades.json", "r") as f:
    state = json.load(f)

print("Balance:", state["balance"])
print("Wins:", state["wins"])
print("Losses:", state["losses"])
print("Open Trade:", state["open_trade"])
